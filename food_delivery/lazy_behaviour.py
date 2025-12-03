from fooddelivery import DriverBehaviour

class LazyBehaviour:
    def __init__(self, max_idle)-> None:
        self.max_idle = max_idle

    def decide(
        self,
        driver: Driver,
        offer: Offer,
        time: int
    ) -> bool:
        return offer.request.wait_time >= self.max_idle