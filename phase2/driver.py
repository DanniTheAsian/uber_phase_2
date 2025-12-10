"""
Driver entities that navigate the map and fulfil delivery requests.
"""

from .behaviour.driver_behaviour import DriverBehaviour
from .point import Point
from .request import Request

ARRIVAL_EPSILON = 1e-3

class Driver:
    """
    Autonomous driver agent that moves across the map and serves requests.

    Each driver tracks its behaviour policy, current status, and completed trip
    history so that policies and analysis can inspect past performance.
    """
    def __init__(self, driver_id: int, position: Point, speed: float, behaviour: DriverBehaviour | None = None, status: str = "IDLE", current_request: Request | None = None, history: list | None = None) -> None:
        """
        Create a driver with an initial position, speed, and behaviour.

        Args:
            driver_id (int): Unique identifier for the driver.
            position (Point): Starting position on the map.
            speed (float): Movement speed in units per simulation tick.
            behaviour (DriverBehaviour | None): Policy controlling acceptance decisions.
            status (str): Initial lifecycle status, defaults to "IDLE".
            current_request (Request | None): Request already assigned to the driver.
            history (list | None): Completed trip history; defaults to an empty list.

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
    
    def assign_request(self, request: Request, assignment_meta: float | None = None, reward: float | None = None) -> None:
        """
        Assign a delivery request to the driver.

        Stores the driver's position for distance calculations, updates the
        status to ``TO_PICKUP``, and marks the request as assigned.

        Args:
            request (Request): Delivery request to assign.
            assignment_meta (float | None): Optional legacy metadata, such as the
                simulation tick when the assignment was made.
            reward (float | None): Reward associated with the offer; defaults to 0.0.

        Returns:
            None
        """
        self.position_at_assignment = self.position
        self.current_request = request
        if reward is None and isinstance(assignment_meta, (int, float)):
            # Compatibility: older call sites pass current simulation time as the second argument.
            self.assigned_reward = 0.0
        else:
            self.assigned_reward = reward if reward is not None else 0.0
        self.status = "TO_PICKUP"
        request.mark_assigned(self.id)

    def _is_at_target(self, target: Point | None) -> bool:
        """
        Determine whether the driver is within the arrival epsilon of a target.

        Args:
            target (Point | None): Destination to compare against.

        Returns:
            bool: True when the driver is effectively at the target.
        """
        if target is None or self.position is None:
            return False
        return self.position.distance_to(target) <= ARRIVAL_EPSILON

    def at_pickup(self) -> bool:
        """
        Check whether the driver has arrived at the pickup location.

        Returns:
            bool: True when the driver is heading to pickup and has arrived.
        """
        if not self.current_request or self.status != "TO_PICKUP":
            return False
        return self._is_at_target(self.current_request.pickup)

    def at_dropoff(self) -> bool:
        """
        Check whether the driver has arrived at the dropoff location.

        Returns:
            bool: True when the driver is heading to dropoff and has arrived.
        """
        if not self.current_request or self.status != "TO_DROPOFF":
            return False
        return self._is_at_target(self.current_request.dropoff)

    def target_point(self) -> Point | None:
        """
        Return the driver's current navigation target.

        Returns:
            Point | None: Pickup, dropoff, or None when idle.
        """
        if self.current_request is None or self.status == "IDLE":
            return None
        
        if self.status == "TO_PICKUP":
            return self.current_request.pickup
        
        if self.status == "TO_DROPOFF":
            return self.current_request.dropoff
        
        return None # returns None for unexpected status.

    def step(self, dt: float) -> None:
        """
        Move the driver towards its current target.

        The driver advances at its configured speed for the provided time step
        and snaps to the destination if it would overshoot.

        Args:
            dt (float): Time step duration in simulation ticks.

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
        """
        Finish the pickup process and transition to dropoff.

        Args:
            time (int): Simulation tick when the pickup completes.

        Returns:
            None
        """

        if self.current_request and self.status == "TO_PICKUP":
            self.status = "TO_DROPOFF"
            self.current_request.mark_picked(time)
        
    def complete_dropoff(self, time:int) -> None:
        """
        Finish the dropoff process and record the completed trip.

        Args:
            time (int): Simulation tick when the dropoff completes.

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
            earnings = self.assigned_reward

            self.history.append({
                "driver_id": self.id,
                "request_id": self.current_request.id,
                "completion_time": time,
                "earnings": earnings,
                "total_distance": total_distance
            })
                            
            self.current_request = None
            self.status = "IDLE"
            self.position_at_assignment = None
            self.assigned_reward = 0.0
