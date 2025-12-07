""" 
This module contains the Driver class which represents 
an autonomous driver agent in the simulation system.
"""

from driver_behaviour import DriverBehaviour
from point import Point
from request import Request

class Driver:
    """
    An autonomous driver agent in the system 
    where each driver can move on the map,
    accept or reject requests based on their behaviour policy,
    and maintain a history of completed trips for statistics.
    """
    def __init__(self, id: int, position: Point, speed: float, behaviour: DriverBehaviour, status: str = "IDLE", current_request: Request | None = None, history: list | None = None) -> None:
        """ Initialize Driver instance

        Args:
            id (int): Unique identifier for the driver
            position (Point): Starting position on the map.
            speed (float): Movement speed in units per simulation tick.
            behaviour (DriverBehaviour): Decision Policy for accepting or rejecting requests.
            status (str, optional): Initial status of the driver. Defaults to "IDLE".
            current_request (Request | None, optional): Current assigned request. Defaults to None.
            history (list | None, optional): List of completed trips for statistics. Defaults to None which initializes an empty list.
         
        Returns:
            None
        """
        self.id = id
        self.position = position
        self.speed = speed
        self.behaviour = behaviour
        self.status = status
        self.current_request = current_request
        self.position_at_assignment: Point | None = None

        if not history:
            self.history = []
        else:
            self.history = history
    
    def assign_request(self, request: Request) -> None:
        """ Assign a delivery request to the driver.
        
        Stores the driver's current position for distance calculation,
        updates the driver's status to TO_PICKUP, and marks the request
        as assigned to this driver.
        
        Args:
            request (Request): The delivery request to assign.
        
        Returns:
            None
        """
        self.position_at_assignment = self.position
        self.current_request = request
        self.status = "TO_PICKUP"
        request.mark_assigned(self.id)

    def target_point(self) -> Point | None:
        """ Get the driver's current target destination.
        
        Returns:
            Point | None: The pickup point if status is TO_PICKUP,
                         the dropoff point if status is TO_DROPOFF,
                         or None if the driver is idle or has no request.
        """
        if self.current_request is None or self.status == "IDLE":
            return None
        
        if self.status == "TO_PICKUP":
            return self.current_request.pickup
        
        if self.status == "TO_DROPOFF":
            return self.current_request.dropoff
        
        return None # returns None for unexpected status.

    def step(self, dt: float) -> None:
        """ Move the driver towards its current target.
        
        The driver moves at its speed for the given time step. If the
        target is within reach, the driver arrives exactly at the target.
        
        Args:
            dt (float): Time step duration.
        
        Returns:
            None
        """

        destination = self.target_point()

        if destination is None:
            return
        
        distance = self.position.distance_to(destination)
        movement = self.speed * dt

        if distance <= movement:
            self.position = destination
        else:
            ratio = movement / distance
            direction = destination - self.position
            travel = direction * ratio
            self.position += travel

    def complete_pickup(self, time: int) -> None:
        """ The driver completes the pickup process, 
            updates its status to TO_DROPOFF 
            and marks the request as picked.

            Args:
                time (int): The current simulation time tick.
            Returns:
                None
        """

        if self.current_request and self.status == "TO_PICKUP":
            self.status = "TO_DROPOFF"
            self.current_request.mark_picked(time)
        
    def complete_dropoff(self, time:int) -> None:
        """ The driver completes the dropoff process, 
            updates its status to IDLE, 
            marks the request as delivered,
            and records the trip in history.
            
            Args:
                time (int): The current simulation time tick when dropoff is completed.
            
            Returns:
                None
        """
        if self.current_request and self.status == "TO_DROPOFF" and self.position_at_assignment is not None:
            self.current_request.mark_delivered(time)

            pickup_position = self.current_request.pickup
            dropoff_position = self.current_request.dropoff

            distance_to_pickup = self.position_at_assignment.distance_to(pickup_position)
            distance_from_pickup_to_dropoff = pickup_position.distance_to(dropoff_position)

            total_distance = distance_to_pickup + distance_from_pickup_to_dropoff

            # TODO: REMEMBER TO CHANGE THIS to the reward system
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
