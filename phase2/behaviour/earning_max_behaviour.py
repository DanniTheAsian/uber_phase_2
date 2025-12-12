"""
Earning-maximising driver behaviour.

This behaviour accepts offers when the expected reward per unit of travel
time exceeds a configurable threshold (optionally adjusted by time).
"""

from .driver_behaviour import DriverBehaviour


class EarningMaxBehaviour(DriverBehaviour):
    """
    A behaviour that accepts offers only if the reward-to-time ratio
    is above a certain minimum.

    The idea is that a driver will accept an offer only if the expected
    earning per unit of travel time is high enough.

    Attributes:
        min_ratio (float): The minimum required reward/travel_time ratio
    """
    def __init__(self, min_ratio):
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
        Decide whether the driver accepts the offer.

        The driver compares the earning-per-time ratio:
            ratio = reward / travel_time

        As the simulation time increases, the driver becomes slightly more picky.
        This is done by increasing the required threshold a little over time.

            effective_threshold = min_ratio * (1 + 0.0005 * time)

        Args:
            driver (Driver): The driver making the decision.
            offer (Offer): Contains estimated_reward and travel_time.
            time (int): Current simulation time.

        Returns:
            bool: True if the offer is accepted.
        
        Note:
            - Returns False if estimated_reward is None
            - Returns False if travel_time is 0 (avoid division by zero)
            - Uses time-adjusted threshold: min_ratio * (1 + 0.0005 * time)
        """

        if offer.estimated_reward is None:
            return False
        
        if offer.estimated_travel_time <= 0:
            return False
        
        threshold = self.min_ratio * (1 + 0.0005 * time)
        
        ratio = offer.estimated_reward / offer.estimated_travel_time
        return ratio >= threshold

    # for debugging
    def __repr__(self) -> str:
        """String representation of the behaviour."""

        return f"EarningMaxBehaviour(min_ratio={self.min_ratio})"
    