from food_delivery.driver_behaviour import DriverBehaviour

class GreedyDistanceBehaviour(DriverBehaviour):
    def __init__(self, max_distance: float):
        self.max_distance = max_distance

    def decide(self, driver: "Driver", offer: "Offer", time: int) -> bool:
        pickup_point = offer.request.pickup
        distance = driver.position.distance_to(pickup_point)
        return distance < self.max_distance
