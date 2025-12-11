"""
Driver behaviour that accepts requests based on maximum pickup distance.
"""

from .driver_behaviour import DriverBehaviour


class GreedyDistanceBehaviour(DriverBehaviour):
    """
    A behaviour where the driver accepts the offer if the pickup location
    is closer than a given maximum distance.
    """
    def __init__(self, max_distance: float) -> None:
        """
        Initialize the behaviour with a maximum allowed pickup distance.

        Args:
            max_distance (float): Maximum pickup distance the driver is willing to accept.

        Returns:
            None

        Example:
                >>> b = GreedyDistanceBehaviour(10.0)
                >>> b.max_distance
                10.0
            """
        self.max_distance = max_distance

    def decide(self, driver: 'Driver', offer: 'Offer', time: int) -> bool:
        """
        Decide whether the driver accepts the offer.

        The driver measures the distance from their current position
        to the pickup point and accepts the offer if the distance is
        below the configured maximum.

        Args:
            driver (Driver): The driver making the decision.
            offer (Offer): Contains the request and its pickup position.
            time (int): Current simulation time (not used here).

        Returns:
            bool: True if pickup distance is below max_distance.
        """
        try:
            pickup_point = offer.request.pickup
            distance = driver.position.distance_to(pickup_point)
        except (AttributeError, TypeError, ValueError) as err:
            print(f"GreedyDistanceBehaviour error: {err}")
            return False

        return distance < self.max_distance