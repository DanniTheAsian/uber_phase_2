"""docstring"""

from typing import List, Tuple
from .driver import Driver
from .request import Request
from .policies.dispatch_policy import DispatchPolicy
from .request_generator import RequestGenerator  
from .mutationrule import mutationrule          
from .offer import Offer


class DeliverySimulation:

    def __init__(
        self,
        drivers: List[Driver],
        requests: List[Request],
        dispatch_policy: DispatchPolicy,
        request_generator: RequestGenerator,
        mutation_rule: mutationrule,
        timeout: int,
    ) -> None:
        """Initialize a DeliverySimulation instance.
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
        self.mutation_rule = mutation_rule

        self.served_count: int = 0
        self.expired_count: int = 0
        self.total_wait_time: int = 0
        self.completed_deliveries: int = 0

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
        new_requests: List[Request] = self.request_generator.maybe_generate(self.time) or []
        if new_requests:
            self.requests.extend(new_requests)

        # 2) Update waiting times and mark expired requests
        active_requests: List[Request] = []
        for req in self.requests:
            if req.is_active():
                req.update_wait(self.time)
                if req.wait_time > self.timeout and req.status != "EXPIRED":
                    req.mark_expired(self.time)
                    self.expired_count += 1
                else:
                    if req.status in ("WAITING", "ASSIGNED", "PICKED"):
                        active_requests.append(req)

        # 3) Compute proposed assignments via dispatch_policy
        proposals: List[Tuple[Driver, Request]] = self.dispatch_policy.assign(
            self.drivers, active_requests, self.time
        ) or []

        # 4) Convert proposals to offers, ask driver behaviours to accept/reject
        accepted: List[Tuple[Driver, Request]] = []
        for item in proposals:
            if not (isinstance(item, tuple) and len(item) >= 2):
                continue
            driver, req = item[0], item[1]

            try:
                dist = driver.position.distance_to(req.pickup)
                est_time = dist / (driver.speed or 1)
            except Exception:
                est_time = 0.0

            offer = Offer(driver=driver, request=req, estimated_travel_time=est_time)
            if driver.behaviour.decide(driver, offer, self.time):
                accepted.append((driver, req))

        # 5) Resolve conflicts and finalise assignments (first-come, first-served)
        used_requests = set()
        for driver, req in accepted:
            if req in used_requests or req.status == "ASSIGNED":
                continue
            driver.assign_request(req, self.time)
            used_requests.add(req)

        # 6) Move drivers and handle pickup/dropoff events
        for driver in self.drivers:
            driver.step(1.0)

            if driver.at_pickup():
                driver.complete_pickup(self.time)

            if driver.at_dropoff():
                delivered_req = driver.complete_dropoff(self.time)
                if delivered_req is None:
                    delivered_req = getattr(driver, "current_request", None)
                if delivered_req:
                    self.served_count += 1
                    self.completed_deliveries += 1
                    self.total_wait_time += getattr(delivered_req, "wait_time", 0)

        # 7) Apply mutation_rule to each driver
        for driver in self.drivers:
            self.mutation_rule.maybe_mutate(driver, self.time)

        # 8) Increment time
        self.time += 1

    def get_snapshot(self) -> dict:
        """Return a state snapshot for the GUI."""
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