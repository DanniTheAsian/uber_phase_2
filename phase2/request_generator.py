import random
from phase2.request import Request
from phase2.point import Point


class RequestGenerator:
    """
    Generates new Request objects over time.

    The generator is called once per simulation tick and creates new
    requests according to a fixed average rate. A random number is drawn
    at each tick to determine whether a new request should be generated.
    """

    def __init__(self, rate: float, width: int, height: int):
        """
        Initialize the request generator.

        Args:
            rate (float): Expected number of new requests per tick.
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

        This method is called once per tick. A random number is drawn and
        compared to the configured rate. If the draw is below the rate,
        a new Request object is created with valid pickup and dropoff
        positions within the map.

        Args:
            time (int): Current simulation time (tick).

        Returns:
            list[Request]: A list containing zero or one newly generated
            Request objects.
        """
        new_requests = []

        if random.random() < self.rate:
            pickup = Point(
                random.uniform(0, self.width),
                random.uniform(0, self.height),
            )
            dropoff = Point(
                random.uniform(0, self.width),
                random.uniform(0, self.height),
            )

            new_requests.append(
                Request(
                    id=self.next_id,
                    pickup=pickup,
                    dropoff=dropoff,
                    creation_time=time,
                )
            )
            self.next_id += 1

        return new_requests
