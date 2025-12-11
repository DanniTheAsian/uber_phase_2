from .driver import Driver
from .request import Request
from .offer import Offer
from .mutationrule.mutationrule import MutationRule
from .policies.dispatch_policy import DispatchPolicy
from .request_generator import RequestGenerator

class DeliverySimulation:
    def __init__(self,
                 drivers: list[Driver],
                 requests: list[Request],
                 dispatch_policy: DispatchPolicy,
                 request_generator: RequestGenerator,
                 mutation_rule: MutationRule,
                 timeout: int,
                 base_reward: float = 25.0,    
                 distance_rate: float = 0.2
                 ) -> None:
        
        self.time: int = 0
        self.timeout: int = timeout
        
        self.drivers = drivers
        self.requests = requests
        self.dispatch_policy = dispatch_policy
        self.request_generator = request_generator
        self.mutation_rule = mutation_rule

        # Reward System
        self.base_reward = base_reward
        self.distance_rate = distance_rate

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
        
        # Searching all idle drivers and all waiting requests
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
            
            reward = self._calculate_reward(driver, request)
            
            offer = Offer(driver, request, estimated_time, reward)

            # Ask driver if they accept (if they have behaviour)
            if driver.behaviour and driver.behaviour.decide(driver, offer, self.time):
                accepted_offers.append((driver, request))


        # 5. Resolve conflicts and finalise assignments.
        assigned_requests = set()

        for driver, request, payment in accepted_offers:
            if request in assigned_requests:
                continue
            if request.status != "WAITING":
                continue

            try:
                driver.assign_request(request, payment)
                assigned_requests.add(request)

            except Exception as e:
                print(f"Assignment failed: {e}")
                continue


        # 6. Move drivers and handle pickup/dropoff events.
        for driver in self.drivers:
            
            driver.step(dt = 1.0)
            
            # Check pickup
            if driver.status == "TO_PICKUP" and driver.current_request and driver.position == driver.current_request.pickup:
                
                driver.complete_pickup(self.time)
            
            # Check dropoff
            if driver.status == "TO_DROPOFF" and driver.current_request and driver.position == driver.current_request.dropoff:

                delivered_request = driver.current_request
                driver.complete_dropoff(self.time)
                
                if delivered_request:
                    self.served_count += 1
                    self.completed_deliveries += 1
                    self.total_wait_time += delivered_request.wait_time


        # 7. Apply mutation_rule
        for driver in self.drivers:
            self.mutation_rule.maybe_mutate(driver, self.time)

        # 8. Increment time.
        self.time += 1


    def get_snapshot(self) -> dict:
        drivers_data = []
        
        for driver in self.drivers:
            driver_info = {
                "id": driver.id,
                "x": driver.position.x,
                "y": driver.position.y,
                "status": driver.status
            }
            drivers_data.append(driver_info)

            
        pickup_positions = []
        dropoff_positions = []
        for request in self.requests:
            if request.status in ("WAITING", "ASSIGNED"):
                pickup_positions.append((request.pickup.x, request.pickup.y))
            elif request.status == "PICKED":
                dropoff_positions.append((request.dropoff.x, request.dropoff.y))
       
        if self.completed_deliveries > 0:
            avg_wait = self.total_wait_time / self.completed_deliveries
        else:
            avg_wait = 0.0


        stats = {
            "served": self.served_count,
            "expired": self.expired_count,
            "avg_wait": avg_wait
        }
        
        snapshot = {
            "time": self.time,
            "drivers": drivers_data,
            "pickups": pickup_positions,
            "dropoffs": dropoff_positions,
            "statistics": stats
        }
        
        return snapshot

    def _calculate_reward(self, driver: Driver, request: Request) -> float:
        """
        Calculate reward for driver accepting a request.
        
        Formula: base_reward + (distance * distance_rate)
        
        Args:
            driver: The driver who might accept
            request: The request being considered
            
        Returns:
            float: Reward amount in points
        """

        distance = driver.position.distance_to(request.pickup)

        return self.base_reward + distance * self.distance_rate
