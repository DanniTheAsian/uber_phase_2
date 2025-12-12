"""
Driver behaviour that accepts offers based on a minimum reward-to-time ratio.
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
        
        Notes:
            - Returns False if estimated_reward is None
            - Returns False if travel_time is 0 (avoid division by zero)
            - Uses time-adjusted threshold: min_ratio * (1 + 0.0005 * time)
        """

        try:
            reward = offer.estimated_reward
            travel_time = offer.estimated_travel_time
        except (AttributeError, TypeError) as err:
            print(f"EarningMaxBehaviour offer error: {err}")
            return False

        if reward is None:
            return False

        try:
            travel_time_value = float(travel_time)
        except (TypeError, ValueError) as err:
            print(f"EarningMaxBehaviour travel time error: {err}")
            return False

        if travel_time_value <= 0:
            return False

        try:
            base_ratio = float(self.min_ratio)
        except (TypeError, ValueError) as err:
            print(f"EarningMaxBehaviour ratio error: {err}")
            return False

        threshold = base_ratio * (1 + 0.0005 * time)

        try:
            ratio = float(reward) / travel_time_value
        except (TypeError, ValueError, ZeroDivisionError) as err:
            print(f"EarningMaxBehaviour ratio calc error: {err}")
            return False

        return ratio >= threshold

    def __repr__(self) -> str:
        """String representation of the behaviour."""

        return f"EarningMaxBehaviour(min_ratio={self.min_ratio})"
    