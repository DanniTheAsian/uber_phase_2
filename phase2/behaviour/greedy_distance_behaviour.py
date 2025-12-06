from phase2.behaviour.driver_behaviour import DriverBehaviour

class GreedyDistanceBehaviour(DriverBehaviour):
    """
    A behaviour where the driver accepts the offer if the pickup location
    is closer than a given maximum distance.
    """
    def __init__(self, max_distance: float) -> None:
        """
        Initialize the behaviour with a maximum allowed pickup distance.

        Arguments:
            max_distance (float): The farthest distance the driver will accept.

        Return:
            None

        Example:
            >>> b = GreedyDistanceBehaviour(10.0)
            >>> b.max_distance
            10.0
        """
        self.max_distance = max_distance

    def decide(self, driver: "Driver", offer: "Offer", time: int) -> bool:
        """
                Decide whether the driver accepts the offer.

        The driver measures the distance from their current position
        to the pickup point and accepts the offer if the distance is
        below the configured maximum.

        Arguments:
            driver (Driver): The driver making the decision.
            offer (Offer): Contains the request and its pickup position.
            time (int): Current simulation time (not used here).

        Returns:
            bool: True if pickup distance is below max_distance.

        Example:
            >>> class MockPoint:
            ...     def __init__(self, x, y): self.x, self.y = x, y
            ...     def distance_to(self, other):
            ...         return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
            >>> class MockRequest:
            ...     def __init__(self, p): self.pickup = p
            >>> class MockOffer:
            ...     def __init__(self, req): self.request = req
            >>> class MockDriver:
            ...     def __init__(self, pos): self.position = pos

            >>> behaviour = GreedyDistanceBehaviour(5.0)
            >>> driver = MockDriver(MockPoint(0, 0))
            >>> offer = MockOffer(MockRequest(MockPoint(3, 4)))  # distance = 5

            # distance == 5, max_distance == 5 → False (strictly less)
            >>> behaviour.decide(driver, offer, time=0)
            False
        """
        pickup_point = offer.request.pickup
        distance = driver.position.distance_to(pickup_point)
        return distance < self.max_distance
