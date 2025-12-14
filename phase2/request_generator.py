"""
Request generation utilities.

This module provides the RequestGenerator class which creates new
Request objects over time according to a configured rate and a simple
time-dependent model. The generator produces pickup/dropoff points
within the simulator's map bounds.
"""

import random
from phase2.request import Request
from phase2.point import Point

class RequestGenerator:
    """
    Generates zero or more new Request objects based on the generator's rate.
    The simulation time is used to model time-dependent request rates,
    enabling scenarios such as rush-hour effects.

    For simplicity, the request rate is increased during a specific time
    window (e.g., between ticks 200 and 300). Outside this window, the
    normal rate applies.
    """

    def __init__(self, rate:float, width:int, height: int):

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
        new_requests: list[Request] = []

        try:
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
                try:
                    req = Request(id=self.next_id, pickup=pickup, dropoff=dropoff, creation_time=time)
                except (TypeError, ValueError) as err:
                    print(f"Request construction error at time {time}: {err}")
                    continue
                self.next_id += 1
                new_requests.append(req)

        except (AttributeError, TypeError, ValueError, ZeroDivisionError) as err:
            print(f"RequestGenerator error at time {time}: {err}")

        return new_requests