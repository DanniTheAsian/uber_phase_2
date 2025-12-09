from .driver_behaviour import DriverBehaviour


class LazyBehaviour(DriverBehaviour):
    """
    A behaviour where the driver only accepts a request if it has been
    waiting long enough. The driver is "lazy" and prefers not to take
    new requests unless they have already waited for a certain amount
    of time.
    """
    def __init__(self, max_idle)-> None:
        """
        Initialize the behaviour with a required minimum wait time.

        Arguments:
            max_idle (int): The minimum wait_time a request must have
                            before the driver accepts it.

        Example:
            >>> b = LazyBehaviour(10)
            >>> b.max_idle
            10
        """
        self.max_idle = max_idle

    def decide(self, driver: 'Driver', offer: 'Offer', time: int) -> bool:
        """
        Decide whether the driver accepts the offer.

        The driver accepts the request only if the request's wait_time
        is equal to or greater than the configured threshold.

        Arguments:
            driver (Driver): The driver making the decision.
            offer (Offer): Contains the request with its wait_time.
            time (int): Current simulation time (not used here).

        Returns:
            bool: True if request.wait_time >= max_idle, otherwise False.
        """
        
        return offer.request.wait_time >= self.max_idle