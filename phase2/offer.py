"""
This module defines the offer class which represents
a suggested assignment between a driver and a request
"""

class Offer:
    """
    Represents an offer given to a driver to fulfill a request.

    An offer links a driver to a request along with estimated
    travel time and an optional estimated reward for completing
    the request.
    """

    def __init__(self,
                 driver: 'Driver',
                 request: 'Request',
                 estimated_travel_time: float,
                 estimated_reward: float | None = None) -> None:
        """Initialize an Offer instance.
        
        Args:
            driver (Driver): The driver receiving the offer.
            request (Request): The request the offer is for.
            estimated_travel_time (float): Estimated time it takes in simulation ticks.
            estimated_reward (float | None): Optional estimated reward for completing the request.
        """
        self.driver = driver
        self.request = request
        self.estimated_travel_time = estimated_travel_time
        self.estimated_reward = estimated_reward