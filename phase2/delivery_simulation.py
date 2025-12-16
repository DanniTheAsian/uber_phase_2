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
            dispatch_policy (DispatchPolicy): Strategy for driver–request assignment.
            request_generator (RequestGenerator): Generates new requests over time.
            mutation_rules (list[MutationRule]): Rules that update driver behaviour over time.
            timeout (int): Maximum wait time before a request expires.

        This constructor also initializes simulation statistics and the
        simulation clock.
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
        self.current_policy_name = dispatch_policy.__class__.__name__

    def tick(self) -> None:
        """
        Advance the simulation by one time step.

        This method orchestrates the simulation pipeline by delegating
        each step to dedicated helper methods. The main steps are:

        1. Generate new requests.
        2. Update waiting times and expire overdue requests.
        3. Propose driver–request assignments using the dispatch policy.
        4. Convert proposals into offers and evaluate driver decisions.
        5. Finalize accepted assignments.
        6. Move drivers and handle pickup and dropoff events.
        7. Apply mutation rules to drivers.
        8. Update time and log simulation metrics.
        """

        self._generate_new_requests()
        active_requests = self._update_waiting_time()
        proposals = self._propose_assignments(active_requests)
        accepted = self._process_offers(proposals)
        self._finalize_assigments(accepted)
        self._move_drivers_and_handle_events()

        # Apply mutation rules to each driver
        active_drivers = 0
        behaviour_counts = {}

        for driver in self.drivers:
            for rule in self.mutation_rules:
                try:
                    rule.maybe_mutate(driver, self.time)
                except (AttributeError, TypeError, ValueError) as err:
                    print(f"Mutation error at time {self.time}: {err}")
            
            # Count behaviour
            if driver.behaviour is None:
                behaviour_name = "no_behaviour"
            else:
                behaviour_name = driver.behaviour.__class__.__name__
            
            if behaviour_name in behaviour_counts:
                current_count = behaviour_counts[behaviour_name]
                new_count = current_count + 1
                behaviour_counts[behaviour_name] = new_count
            else:
                behaviour_counts[behaviour_name] = 1
            
            # Count active drivers
            if driver.status != "IDLE":
                active_drivers += 1

        # 8) Increment time
        self.time += 1

        # Log metrics for plotting
        if self.completed_deliveries > 0:
            avg_wait = self.total_wait_time / self.completed_deliveries
        else:
            avg_wait = 0.0

        current_policy_name = self.dispatch_policy.__class__.__name__
        if current_policy_name != self.current_policy_name:
            self.current_policy_name = current_policy_name
            print(f"Policy change to: {self.current_policy_name} at time {self.time}")

        self.metrics_log.append({
            'time': self.time,
            'served': self.served_count,
            'expired': self.expired_count,
            'avg_wait': avg_wait,
            'active_drivers': active_drivers,
            'behaviour_counts': behaviour_counts,
            'policy': current_policy_name
        })

    def get_snapshot(self) -> dict:
        """
        Return a state snapshot for the GUI.
        """

        drivers_snapshot = []
        for driver in self.drivers:
            pos = driver.position
            drivers_snapshot.append({
                "id": driver.id,
                "x": pos.x if pos else None,
                "y": pos.y if pos else None,
                "status": driver.status,
            })

        pickups = [request.pickup for request in self.requests if request.status in ("WAITING", "ASSIGNED")]
        dropoffs = [request.dropoff for request in self.requests if request.status == "PICKED"]

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
        """Generate new requests using the request generator."""
        try:
            new_requests: List[Request] = self.request_generator.maybe_generate(self.time)
            if new_requests is None:
                new_requests = []
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
        for request in self.requests:
            if request.status == "WAITING":
                request.update_wait(self.time)
                if request.wait_time > self.timeout:
                    request.mark_expired(self.time)
                    self.expired_count += 1
                else:
                    waiting_requests.append(request)
        return waiting_requests


    def _propose_assignments(self, active_requests: List[Request]) -> List[Tuple[Driver, Request]]:
        """
        Ask the dispatch policy to propose driver–request assignments.
        """

        if self.dispatch_policy is None:
            return []
        try:
            proposals = self.dispatch_policy.assign(self.drivers, active_requests, self.time)
            if proposals is None:
                proposals = []
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Dispatch policy error at time {self.time}: {err}")
            proposals = []
        return proposals


    def _process_offers(self, proposals: List[Tuple[Driver, Request]]) -> List[Tuple[Driver, Request]]:
        """Create offers from proposals and collect accepted ones."""
        accepted = []
        for driver, request in proposals:
            try:
                distance_to_pickup = driver.position.distance_to(request.pickup)
                estimated_travel_time = distance_to_pickup / max(driver.speed, 0.1)
                distance_pickup_to_dropoff = request.pickup.distance_to(request.dropoff)
                total_distance = distance_to_pickup + distance_pickup_to_dropoff

                base_reward = 15.0
                distance_bonus = 1.5 * total_distance
                estimated_reward = base_reward + distance_bonus

                offer = Offer(driver, request, estimated_travel_time, estimated_reward)
            except (AttributeError, TypeError, ValueError, ZeroDivisionError) as err:
                print(f"Offer creation error for driver/req at time {self.time}: {err}")
                continue

            try:
                decision = driver.behaviour.decide(driver, offer, self.time)

            except (TypeError, ValueError) as err:
                print(f"Behaviour decision error for driver {driver.id} and request {request.id} at time {self.time}: {err}")
                
                decision = False

            if decision:
                accepted.append((driver, request))

        return accepted

    def _finalize_assigments(self, accepted: List[Tuple[Driver, Request]]) -> None:
        """Finalize accepted assignments while avoiding conflicts."""
        used_requests = set()
        used_drivers = set()
        for driver, request in accepted:
            if request in used_requests or driver in used_drivers or request.status == "ASSIGNED":
                continue
            try:
                driver.assign_request(request, self.time)
                used_requests.add(request)
                used_drivers.add(driver)
            except (AttributeError, TypeError, ValueError) as err:
                print(f"Error finalizing assignment at time {self.time}: {err}")

    def _move_drivers_and_handle_events(self) -> None:
        """Move drivers and handle pickup and dropoff events."""
        for driver in self.drivers:
            driver.step(1.0)

            # arrival detection: check proximity to pickup/dropoff points
            if driver.current_request and driver.status == "TO_PICKUP":
                if driver.position.distance_to(driver.current_request.pickup) < 1e-6:
                    driver.complete_pickup(self.time)

            if driver.current_request and driver.status == "TO_DROPOFF":
                if driver.position.distance_to(driver.current_request.dropoff) < 1e-6:
                    # capture request reference before completion clears it
                    request = driver.current_request
                    driver.complete_dropoff(self.time)
                    if request:
                        self.served_count += 1
                        self.completed_deliveries += 1
                        try:
                            self.total_wait_time += request.wait_time
                        except (AttributeError, TypeError):
                            pass