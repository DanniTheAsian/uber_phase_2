from .driver import Driver
from .request import Request
from .offer import Offer
from .policies.dispatch_policy import DispatchPolicy
from .request_generator import RequestGenerator
from .mutationrule.mutationrule import MutationRule


class DeliverySimulation:
    def __init__(self,
                 drivers: list[Driver],
                 requests: list[Request],
                 dispatch_policy: DispatchPolicy,
                 request_generator: RequestGenerator,
                 mutation_rule: MutationRule,
                 timeout: int,
                 ) -> None:
        
        self.time: int = 0
        self.timeout: int = timeout
        
        self.drivers = drivers
        self.requests = requests
        self.dispatch_policy = dispatch_policy
        self.request_generator = request_generator
        self.mutation_rule = mutation_rule

        # Statistics
        self.served_count: int = 0
        self.expired_count: int = 0
        self.total_wait_time: int = 0
        self.completed_deliveries: int = 0
    
    def tick(self) -> None:
        """Advance the simulation by one time step."""

        # 1. Generate new requests.
        new_requests = self.request_generator.maybe_generate(self.time)
        if new_requests:
            self.requests.extend(new_requests)

        # 2. Update waiting times and mark expired requests.
        active_requests = []
        for req in self.requests:
            if req.is_active():
                # Update wait time
                req.update_wait(self.time)
                
                # Check if expired
                if req.wait_time > self.timeout and req.status != "EXPIRED":
                    req.mark_expired(self.time)
                    self.expired_count += 1
                else:
                    # Keep in active list for Step 3
                    if req.status in ("WAITING", "ASSIGNED", "PICKED"):
                        active_requests.append(req)
              
        # 3. Compute proposed assignments via dispatch_policy.
        
        # find all idle drivers and all waiting requests
        idle_drivers = [d for d in self.drivers if d.status == "IDLE"]
        waiting_requests = [r for r in active_requests if r.status == "WAITING"]
    
        proposals = self.dispatch_policy.assign(
            idle_drivers,
            waiting_requests,
            self.time
        )
        # proposals returns a list[tuple[Driver, Request]]

        # 4. Convert proposals to offers, ask driver behaviours to accept/reject.
        accepted_offers = []
        for driver, request in proposals:
            distance = driver.position.distance_to(request.pickup)
            if driver.speed <= 0:
                estimated_time = 0.0
            else:
                estimated_time = distance / driver.speed
            
            offer = Offer(
            driver=driver,
            request=request,
            estimated_travel_time=estimated_time,
            estimated_reward=None
            )

            # Ask driver if they accept (if they have behaviour)
            if driver.behaviour and driver.behaviour.decide(driver, offer, self.time):
                accepted_offers.append((driver, request))


        # 5. Resolve conflicts and finalise assignments.
        # 6. Move drivers and handle pickup/dropoff events.
        # 7. Apply mutation_rule
    

