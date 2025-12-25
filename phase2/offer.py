"""
This module defines the offer class which represents
a suggested assignment between a driver and a request
"""
from dataclasses import dataclass
from .driver import Driver
from .request import Request

@dataclass
class Offer:
    """
    Represents an offer given to a driver to fulfill a request.

    An offer links a driver to a request along with estimated
    travel time and an optional estimated reward for completing
    the request.
    """

    driver: "Driver"
    request: "Request"
    estimated_travel_time: float
    estimated_reward: float | None = None