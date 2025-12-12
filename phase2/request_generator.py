"""
Utilities for generating random delivery requests during the simulation.
"""

import random
from .request import Request
from .point import Point

class RequestGenerator:
    """
    Generate new requests using a random rate and bounded map dimensions.
    The generator keeps track of the map's width and height so that pickup
    and dropoff points always fall within bounds, and it increments
    internal IDs to ensure every request is unique.
    """

    def __init__(self, rate:float, width:int, height: int):
        """
        Initialize the generator with a base rate and rectangular bounds.

        Args:
            rate (float): Probability of spawning a request on each tick.
            width (int): Width of the map for random coordinate sampling.
            height (int): Height of the map for random coordinate sampling.
        """

        self.rate = rate
        self.width = width
        self.height = height
        self.next_id = 1

    def maybe_generate(self, time: int) -> list[Request]:
        """
        Generates zero or more new Request objects based on the given rate.
        The rate is interpreted as requests per minute (60 ticks).
        Each tick generates approximately rate/60 requests on average.
        """
        new_requests = []

        if self.rate <= 0:
            return new_requests

        # Normalize rate to per-tick: rate/60 (since 1 minute = 60 ticks)
        rate_per_tick = self.rate / 60.0

        # Poisson-like: generate base_count requests + 1 more with probability extra_probability
        base_count = int(rate_per_tick)
        extra_probability = rate_per_tick - base_count
        count = base_count
        if random.random() < extra_probability:
            count += 1

        for _ in range(count):
            pickup = Point(random.uniform(0, self.width), random.uniform(0, self.height))
            dropoff = Point(random.uniform(0, self.width), random.uniform(0, self.height))
            req = Request(id=self.next_id, pickup=pickup, dropoff=dropoff, creation_time=time)
            self.next_id += 1
            new_requests.append(req)

        return new_requests