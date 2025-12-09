import random
from .request import Request
from .point import Point

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
        Time is provided for compatibility with the simulation interface,
        but the Request object does not store it.
        """
        new_requests = []

        if random.random() < self.rate:
            pickup = Point(random.uniform(0, self.width), random.uniform(0, self.height))
            dropoff = Point(random.uniform(0, self.width), random.uniform(0, self.height))

            req = Request(id= self.next_id, pickup=pickup, dropoff=dropoff, creation_time=time)

            self.next_id += 1
            new_requests.append(req)

        return new_requests