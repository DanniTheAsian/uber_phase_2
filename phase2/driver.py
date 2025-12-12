""" 
This module contains the Driver class which represents 
an autonomous driver agent in the simulation system.
"""

from .behaviour.driver_behaviour import DriverBehaviour
from .point import Point
from .request import Request

ARRIVAL_EPSILON = 1e-3

class Driver:
    """
    An autonomous driver agent in the system 
    where each driver can move on the map,
    accept or reject requests based on their behaviour policy,
    and maintain a history of completed trips for statistics.
    """
    def __init__(self, driver_id: int, position: Point, speed: float, behaviour: DriverBehaviour | None = None, status: str = "IDLE", current_request: Request | None = None, history: list | None = None) -> None:
        """
        Initialize Driver instance

        Args:
            driver_id (int): Unique identifier for the driver
            position (Point): Starting position on the map.
            speed (float): Movement speed in units per simulation tick.
            behaviour (DriverBehaviour): Decision Policy for accepting or rejecting requests.
            status (str, optional): Initial status of the driver. Defaults to "IDLE".
            current_request (Request | None, optional): Current assigned request. Defaults to None.
            assigned_reward (float, optional): Reward associated with the assigned request. Defaults to 0.0.
            history (list | None, optional): List of completed trips for statistics. Defaults to None which initializes an empty list.
         
        Returns:
            None
        """
        self.id = driver_id
        self.position = position
        self.speed = speed
        self.behaviour = behaviour
        self.status = status
        self.current_request = current_request
        self.position_at_assignment: Point | None = None
        self.assigned_reward: float = 0.0

        if not history:
            self.history = []
        else:
            self.history = history
    
    def assign_request(self, request: Request, current_time: int) -> None:
        """Assign a delivery request to the driver.

        Records position at assignment, sets current request and status to
        TO_PICKUP and marks the request as assigned.
        """
        self.position_at_assignment = self.position
        self.current_request = request
        # reward estimation not available here; default to 0.0
        self.assigned_reward = 0.0
        self.status = "TO_PICKUP"
        request.mark_assigned(self.id)

    def target_point(self) -> Point | None:
        """
        Get the driver's current target destination.
        
        Returns:
            Point | None: The pickup point if status is TO_PICKUP,
                         the dropoff point if status is TO_DROPOFF,
                         or None if the driver is idle or has no request.
        """
        try:
            request = self.current_request
            status = self.status
        except AttributeError as err:
            print(f"Driver target_point error for driver {self.id}: {err}")
            return None

        if request is None or status == "IDLE":
            return None
        
        try:
            if status == "TO_PICKUP":
                return request.pickup

            if status == "TO_DROPOFF":
                return request.dropoff
        except AttributeError as err:
            print(f"Driver target_point request error for driver {self.id}: {err}")
            return None

        return None # returns None for unexpected status.

    def step(self, dt: float) -> None:
        """
        Move the driver towards its current target.
        
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
        
        try:
            distance = self.position.distance_to(destination)
            movement = self.speed * dt
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Driver step error for driver {self.id}: {err}")
            return

        if distance <= movement:
            self.position = destination
        else:
            try:
                ratio = movement / distance
                direction = destination - self.position
                travel = direction * ratio
                self.position += travel
            except (TypeError, ValueError) as err:
                print(f"Driver movement math error for driver {self.id}: {err}")
                return

    def complete_pickup(self, time: int) -> None:
        """
        The driver completes the pickup process, 
        updates its status to TO_DROPOFF 
        and marks the request as picked.

        Args:
            time (int): The current simulation time tick.
                
        Returns:
            None
        """

        if self.current_request and self.status == "TO_PICKUP":
            self.status = "TO_DROPOFF"
            try:
                self.current_request.mark_picked(time)
            except (AttributeError, TypeError, ValueError) as err:
                print(f"Driver complete_pickup error for driver {self.id}: {err}")
        
    def complete_dropoff(self, time:int) -> None:
        """
        The driver completes the dropoff process, 
        marks the request as delivered,
        records the trip in history,
        clears the current request,
        and its position when the request was received,
        and updates its status to IDLE

        Args:
            time (int): The current simulation time tick when dropoff is completed.
            
        Returns:
            None
        """
        if self.current_request and self.status == "TO_DROPOFF":
            self.current_request.mark_delivered(time)

            pickup_position = self.current_request.pickup
            dropoff_position = self.current_request.dropoff

            # position_at_assignment may be None; guard accordingly
            if self.position_at_assignment is not None:
                distance_to_pickup = self.position_at_assignment.distance_to(pickup_position)
            else:
                distance_to_pickup = 0.0

            distance_from_pickup_to_dropoff = pickup_position.distance_to(dropoff_position)

            total_distance = distance_to_pickup + distance_from_pickup_to_dropoff
            earnings = self.assigned_reward

            self.history.append({
                "driver_id": self.id,
                "request_id": self.current_request.id,
                "completion_time": time,
                "earnings": earnings,
                "total_distance": total_distance,
            })

            self.current_request = None
            self.status = "IDLE"
            self.position_at_assignment = None
            self.assigned_reward = 0.0

    # Note: arrival detection is handled by DeliverySimulation by checking
    # the driver's position against the request pickup/dropoff points.
