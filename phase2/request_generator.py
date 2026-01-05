import random
from phase2.request import Request
from phase2.point import Point


class RequestGenerator:
    """
    Generates new Request objects over time.

    The generator is called once per simulation tick and may generate
    at most one new request per tick. A random draw is used to decide
    whether a request is created.
    """

    def __init__(self, rate: float, width: int, height: int):
        """
        Initialize the request generator.

        Args:
            rate (float): Probability of generating a request per tick (0–1).
            width (int): Width of the map.
            height (int): Height of the map.
        """
        self.rate = rate
        self.width = width
        self.height = height
        self.next_id = 1
 

    def maybe_generate(self, time: int) -> list[Request]:
        """
        Possibly generate a new request at the given simulation time.

        This method is called once per tick. With probability `rate`,
        a single new Request is created with random pickup and dropoff
        locations within the map boundaries.

        Args:
            time (int): Current simulation time (tick).

        Returns:
            list[Request]: A list containing zero or one newly generated request.
        """
        new_requests = []

        base = int(self.rate)
        remainder = self.rate - base 

        for _ in range(base):
            new_requests.append(self._create_request(time))

        if random.random() < remainder:
            new_requests.append(self._create_request(time))
       
        return new_requests


    def _create_request(self, time: int) -> Request:
        """
        Create a single Request with random pickup and dropoff locations.
        """
        pickup = Point(
            random.uniform(0, self.width),
            random.uniform(0, self.height),
        )
        dropoff = Point(
            random.uniform(0, self.width),
            random.uniform(0, self.height),
        )

        request = Request(
            id=self.next_id,
            pickup=pickup,
            dropoff=dropoff,
            creation_time=time,
        )
        self.next_id += 1
        return request