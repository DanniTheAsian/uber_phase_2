""" docstring """

from driver_behaviour import DriverBehavior
from point import Point
from request import Request

class Driver:
    """ docstring """
    def __init__(self, id: int, position: Point, speed: float, behaviour: DriverBehaviour, status: str = "IDLE", current_request: Request | None, history: list) -> None:
        self.id = id
        self.position = position
        self.speed = speed
        self.behavior = behaviour
        self.status = status

        if current_request is None:
            self.current_request = None
        else:
            self.current_request = current_request

        if not history:
            self.history = []
        else:
            self.history = history
    
    def assign_request(self, request: Request) -> None:
        """ docstring """
        self.current_request = request
        self.status = "TO_PICKUP"

    def target_point(self) -> Point | None:
        """ docstring """
        pass

    def step(self, dt: float) -> None:
        pass

    def complete_pickup(self, time: int) -> None:
        pass

    def complete_dropoff(self, time:int) -> None:
        pass



