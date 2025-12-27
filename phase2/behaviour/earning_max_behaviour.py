"""
Earning-maximising driver behaviour.

This behaviour accepts offers when the expected reward per unit of travel
time exceeds a configurable threshold (optionally adjusted by time).
"""


from .driver_behaviour import DriverBehaviour

class EarningMaxBehaviour(DriverBehaviour):
    """
    Decide whether the driver accepts the offer.
    """
    def __init__(self, min_ratio: float = 0.1):
        """
        Initialize the behaviour with a minimum ratio threshold.

        Args:
            min_ratio (float): Minimum acceptable reward/time ratio.

        Example:
            >>> b = EarningMaxBehaviour(2.0)
            >>> b.min_ratio
            2.0
        """
        self.min_ratio = min_ratio

    def decide(self, driver: 'Driver', offer: 'Offer', time: int) -> bool:
        """
        The driver compares the earning-per-time ratio:
            ratio = reward / travel_time

        The driver accepts the offer if:
            ratio >= min_ratio


        Args:
            driver (Driver): The driver making the decision.
            offer (Offer): Contains estimated_reward and travel_time.
            time (int): Current simulation time.

        Returns:
            bool: True if the offer is accepted.
        
        Note:
            - Returns False if estimated_reward is None
            - Returns False if travel_time is 0 (avoid division by zero)
            - min_ratio is a fixed threshold in this implementation.
        """

        if offer.estimated_reward is None:
            return False
        
        if offer.estimated_travel_time <= 0:
            return False
        
        threshold = self.min_ratio
        
        ratio = offer.estimated_reward / offer.estimated_travel_time
        return ratio >= threshold
    