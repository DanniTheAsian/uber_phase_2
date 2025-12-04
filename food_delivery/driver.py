""" docstring """

from point import Point
from request import Request
from driver_behaviour import DriverBehavior

class Driver:
    def __init__(self, id: int, position: Point, speed: float, behaviour: DriverBehaviour, status: str = "IDLE", current_request: Request | None, history: list) -> None:
        self.id = id
        self.position = position
        self.speed = speed
        self.behavior = behaviour
        self.status = status
        self.current_request = current_request
        self.history = history
        

    

