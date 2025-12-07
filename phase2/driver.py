""" docstring """

from driver_behaviour import DriverBehaviour
from point import Point
from request import Request

class Driver:
    """ docstring """
    def __init__(self, id: int, position: Point, speed: float, behaviour: DriverBehaviour, status: str = "IDLE", current_request: Request | None = None, history: list | None = None) -> None:
        """ docstring """
        self.id = id
        self.position = position
        self.speed = speed
        self.behavior = behaviour
        self.status = status
        self.current_request = current_request
        self.position_at_assignment: Point | None = None

        if not history:
            self.history = []
        else:
            self.history = history
    
    def assign_request(self, request: Request) -> None:
        """ docstring """
        self.position_at_assignment = self.position
        self.current_request = request
        self.status = "TO_PICKUP"
        request.mark_assigned(self.id)

    def target_point(self) -> Point | None:
        """ docstring """
        if self.current_request is None or self.status == "IDLE":
            return None
        
        if self.status == "TO_PICKUP":
            return self.current_request.pickup
        
        if self.status == "TO_DROPOFF":
            return self.current_request.dropoff
        
        return None # returns None for unexpected status.

    def step(self, dt: float) -> None:
        """ docstring """

        destination = self.target_point()

        if destination is None:
            return
        
        distance = self.position.distance_to(destination)
        movement = self.speed * dt

        if distance <= movement:
            self.position = destination
        else:
            ratio = movement / distance
            direction = destination - self.position # aka. direction = destination.__sub__(self.position)
            travel = direction * ratio # aka. travel = direction.__mul__(ratio)
            self.position += travel # aka. self.position.__iadd__(travel)

    def complete_pickup(self, time: int) -> None:
        """ docstring """
        if self.current_request and self.status == "TO_PICKUP":
            self.status = "TO_DROPOFF"
            self.current_request.mark_picked(time)
        
    def complete_dropoff(self, time:int) -> None:
        """ docstring """
        if self.current_request and self.status == "TO_DROPOFF" and self.position_at_assignment is not None:
            self.current_request.mark_delivered(time)

            pickup_position = self.current_request.pickup
            dropoff_position = self.current_request.dropoff

            distance_to_pickup = self.position_at_assignment.distance_to(pickup_position)
            distance_from_pickup_to_dropoff = pickup_position.distance_to(dropoff_position)

            total_distance = distance_to_pickup + distance_from_pickup_to_dropoff

            # REMEMBER TO CHANAGE THIS to the reward system
            earnings = total_distance * 2.5

            self.history.append({ 
                "driver_id": self.id,
                "request_id": self.current_request.id,
                "completion_time": time,
                "earnings": earnings,
                "total_distance": total_distance
            })
                   
            self.current_request = None
            self.status = "IDLE"
