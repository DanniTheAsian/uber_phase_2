"""
This module defines the abstract base class for driver behaviours.

A driver behaviour controls how a driver decides whether to accept
an offer in the simulation. Different behaviours (e.g., greedy,
lazy, earning-maximising) inherit from this class and implement
their own decision logic.
"""

from abc import ABC, abstractmethod
from phase2.driver import Driver
from phase2.offer import Offer
class DriverBehaviour(ABC):
    """
    Abstract base class for all driver behaviour types.

    A behaviour determines how a driver reacts to an incoming offer.
    Subclasses must implement the decide() method, which returns
    whether the driver accepts or rejects a given offer.
    """
    @abstractmethod
    def decide(self, driver: 'Driver', offer: 'Offer', time: int) -> bool:
        """
        Decide whether the driver accepts the offer.

        Args:
            driver (Driver): The driver making the decision.
            offer (Offer): The incoming offer containing request info.
            time (int): The current simulation time.

        Returns:
            bool: True if the driver accepts the offer, False otherwise.

        """
