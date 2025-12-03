from food_delivery.driver_behaviour import DriverBehaviour

class LazyBehaviour(DriverBehaviour):
    def __init__(self, max_idle)-> None:
        self.max_idle = max_idle

    def decide(self, driver: "Driver", offer: "Offer", time: int) -> bool:
        return offer.request.wait_time >= self.max_idle