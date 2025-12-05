"""Docstring"""

from phase2.driver import Driver
from phase2.request import Request

class Offer:
    """Docstring"""

    def __init__(self,
                 driver: Driver,
                 request: Request,
                 estimated_travel_time: float,
                 estimated_reward: float | None = None) -> None:
        self.driver = driver
        self.request = request
        self.estimated_travel_time = estimated_travel_time
        self.estimated_reward = estimated_reward