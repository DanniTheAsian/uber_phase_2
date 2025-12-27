"""
Lazy driver behaviour.

This behaviour accepts offers only if the request has waited at least a
configured amount of time and the driver is currently idle.
"""

from .driver_behaviour import DriverBehaviour
from phase2.offer import Offer
from phase2.driver import Driver

class LazyBehaviour(DriverBehaviour):
    """
    A behaviour where the driver only accepts a request if it has been
    waiting long enough. The driver is "lazy" and prefers not to take
    new requests unless they have already waited for a certain amount
    of time.
    """
    def __init__(self, min_wait_time: int = 1)-> None:
        """
        Initialize the behaviour with a required minimum wait time.

        Args:
            min_wait_time (int): The minimum time a request must have
                waited before the driver accepts it.

        Example:
            >>> b = LazyBehaviour(10)
            >>> b.min_wait_time
            10
        """
        self.min_wait_time = min_wait_time

    def decide(self, driver: 'Driver', offer: 'Offer', time: int) -> bool:
        """
        Decide whether the driver accepts the offer.

        The driver accepts the request only if:
        1. The driver is currently IDLE (not on a delivery)
        2. The request's wait_time is equal to or greater than the configured threshold.

        Args:
            driver (Driver): The driver making the decision.
            offer (Offer): Contains the request with its wait_time.
            time (int): Current simulation time (not used here).

        Returns:
            bool: True if driver is IDLE and request.wait_time >= min_wait_time, otherwise False.
        """
        
        return driver.status == "IDLE" and offer.request.wait_time >= self.min_wait_time