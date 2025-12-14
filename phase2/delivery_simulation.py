"""
Delivery simulation core loop and orchestration.

This module implements the DeliverySimulation class which coordinates drivers,
requests, the dispatch policy, the request generator, and mutation rules.
The main simulation step is performed by `tick()` which runs request
generation, waiting-time updates, assignment proposals, offer processing,
driver movement and mutations.
"""

from typing import List, Tuple
from .driver import Driver
from .request import Request
from .policies.dispatch_policy import DispatchPolicy
from .request_generator import RequestGenerator
from .mutationrule.mutationrule import MutationRule
from .offer import Offer


class DeliverySimulation:

    def __init__(
        self,
        drivers: List[Driver],
        requests: List[Request],
        dispatch_policy: DispatchPolicy,
        request_generator: RequestGenerator,
        mutation_rules: List[MutationRule],
        timeout: int,
    ) -> None:
        """
        Initialize a DeliverySimulation instance.

        Args:
            drivers (list[Driver]): All drivers in the simulation.
            requests (list[Request]): Existing requests, both active and completed.
            dispatch_policy (DispatchPolicy): Strategy for driver_request assignment.
            request_generator (RequestGenerator): Generates new requests over time.
            mutation_rule (MutationRule): Updates driver behaviour over time.
            timeout (int): Maximum wait time before a request expires.

        This constructor also initializes global statistics and the simulation clock.
        """

        self.time: int = 0
        self.timeout: int = timeout

        self.drivers = drivers
        self.requests = requests
        self.dispatch_policy = dispatch_policy
        self.request_generator = request_generator
        self.mutation_rules = mutation_rules

        self.served_count: int = 0
        self.expired_count: int = 0
        self.total_wait_time: int = 0
        self.completed_deliveries: int = 0
        # Log for metrics over time
        self.metrics_log = []

    def tick(self) -> None:
        """
        Advance the simulation by one time step.

        This method performs the full 8-step simulation pipeline:
        1. Generate new requests.
        2. Update waiting times and mark expired requests.
        3. Ask the dispatch policy for proposed assignments.
        4. Convert proposals to offers and let drivers accept or reject them.
        5. Resolve conflicts and finalize assignments.
        6. Move drivers and handle pickup/dropoff events.
        7. Apply driver mutation rules.
        8. Increase the simulation time.
        All core simulation logic happens here.
        """

        # 1) Generate new requests
        self._generate_new_requests()
        active_requests = self._update_waiting_time()
        proposals = self._propose_assignments(active_requests)
        accepted = self._process_offers(proposals)
        self._finalize_assigments(accepted)
        self._move_drivers_and_handle_events()

        # 7) Apply mutation rules to each driver
        active_drivers = 0
        behaviour_counts = {}

        for driver in self.drivers:
            for rule in self.mutation_rules:
                try:
                    rule.maybe_mutate(driver, self.time)
                except (AttributeError, TypeError, ValueError) as err:
                    print(f"Mutation error at time {self.time}: {err}")
            
            # Del 2: Count behaviour
            if driver.behaviour is None:
                behaviour_name = "no_behaviour"
            else:
                behaviour_name = driver.behaviour.__class__.__name__
            
            if behaviour_name in behaviour_counts:
                behaviour_counts[behaviour_name] += 1
            else:
                behaviour_counts[behaviour_name] = 1
            
            # Del 3: Count active drivers
            if driver.status != "IDLE":
                active_drivers += 1

        # 8) Increment time
        self.time += 1

        # Log metrics for plotting
        if self.completed_deliveries > 0:
            avg_wait = self.total_wait_time / self.completed_deliveries
        else:
            avg_wait = 0.0

        
        # active_drivers = 0
        # for driver in self.drivers:
          #  if driver.status != "IDLE":
           #     active_drivers += 1

        self.metrics_log.append({
            'time': self.time,
            'served': self.served_count,
            'expired': self.expired_count,
            'avg_wait': avg_wait,
            'active_drivers': active_drivers,
            'behaviour_counts': behaviour_counts
        })

    def get_snapshot(self) -> dict:
        """
        Return a state snapshot for the GUI.
        """

        drivers_snapshot = []
        for d in self.drivers:
            pos = d.position
            drivers_snapshot.append({
                "id": d.id,
                "x": pos.x if pos else None,
                "y": pos.y if pos else None,
                "status": d.status,
            })

        pickups = [r.pickup for r in self.requests if r.status in ("WAITING", "ASSIGNED")]
        dropoffs = [r.dropoff for r in self.requests if r.status == "PICKED"]

        avg_wait = (self.total_wait_time / self.completed_deliveries) if self.completed_deliveries else 0.0

        return {
            "time": self.time,
            "drivers": drivers_snapshot,
            "pickups": pickups,
            "dropoffs": dropoffs,
            "statistics": {
                "served_count": self.served_count,
                "expired_count": self.expired_count,
                "avg_wait": avg_wait,
            }
        }
    
    def _generate_new_requests(self):
        try:
            new_requests: List[Request] = self.request_generator.maybe_generate(self.time) or []
        except (AttributeError, TypeError, ValueError, ZeroDivisionError) as err:
            print(f"Request generation error at time {self.time}: {err}")
            new_requests = []

        if new_requests:
            try:
                self.requests.extend(new_requests)
            except (AttributeError, TypeError, ValueError) as err:
                print(f"Error adding new requests at time {self.time}: {err}")


    def _update_waiting_time(self) -> List[Request]:
        """
        Update waiting times and return only WAITING requests that haven't expired.
        
        This filters to only WAITING requests for assignment proposals.
        ASSIGNED/PICKED requests are handled separately by their drivers.
        """
        waiting_requests: List[Request] = []
        for req in self.requests:
            if req.status == "WAITING":
                req.update_wait(self.time)
                if req.wait_time > self.timeout:
                    req.mark_expired(self.time)
                    self.expired_count += 1
                else:
                    waiting_requests.append(req)
        return waiting_requests


    def _propose_assignments(self, active_requests: List[Request]) -> List[Tuple[Driver, Request]]:
        if self.dispatch_policy is None:
            return []
        try:
            proposals = self.dispatch_policy.assign(self.drivers, active_requests, self.time) or []
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Dispatch policy error at time {self.time}: {err}")
            proposals = []
        return proposals


    def _process_offers(self, proposals: List[Tuple[Driver, Request]]) -> List[Tuple[Driver, Request]]:
        accepted = []
        for driver, req in proposals:
            try:
                dist = driver.position.distance_to(req.pickup)
                est_time = dist / (driver.speed or 1)
                offer = Offer(driver, req, est_time)
            except (AttributeError, TypeError, ValueError, ZeroDivisionError) as err:
                print(f"Offer creation error for driver/req at time {self.time}: {err}")
                continue

            try:
                decision = driver.behaviour.decide(driver, offer, self.time)
            except (AttributeError, TypeError, ValueError) as err:
                print(f"Behaviour decision error for driver/req at time {self.time}: {err}")
                decision = False

            if decision:
                accepted.append((driver, req))

        return accepted

    def _finalize_assigments(self, accepted: List[Tuple[Driver, Request]]) -> None:
        used_requests = set()
        used_drivers = set()
        for driver, req in accepted:
            if req in used_requests or driver in used_drivers or req.status == "ASSIGNED":
                continue
            try:
                driver.assign_request(req, self.time)
                used_requests.add(req)
                used_drivers.add(driver)
            except (AttributeError, TypeError, ValueError) as err:
                print(f"Error finalizing assignment at time {self.time}: {err}")

    def _move_drivers_and_handle_events(self) -> None:
        for driver in self.drivers:
            driver.step(1.0)

            # arrival detection: check proximity to pickup/dropoff points
            if driver.current_request and driver.status == "TO_PICKUP":
                if driver.position.distance_to(driver.current_request.pickup) < 1e-6:
                    driver.complete_pickup(self.time)

            if driver.current_request and driver.status == "TO_DROPOFF":
                if driver.position.distance_to(driver.current_request.dropoff) < 1e-6:
                    # capture request reference before completion clears it
                    req = driver.current_request
                    driver.complete_dropoff(self.time)
                    if req:
                        self.served_count += 1
                        self.completed_deliveries += 1
                        try:
                            self.total_wait_time += req.wait_time
                        except (AttributeError, TypeError):
                            pass