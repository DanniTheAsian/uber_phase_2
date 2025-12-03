from abc import ABC, abstractmethod
class DriverBehavior(ABC):

    @abstractmethod
    def decide(self, driver: Driver, offer: Offer, time: int) -> Bool:
        pass  