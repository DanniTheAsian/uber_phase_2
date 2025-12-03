from abc import ABC, abstractmethod


class DriverBehaviour(ABC):

    @abstractmethod
    def decide(self, driver: "Driver", offer: "Offer", time: int) -> bool:
        pass  