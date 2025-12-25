"""
This module contains the Driver class which represents
an autonomous driver agent in the simulation system.
"""

from dataclasses import dataclass, field
from .behaviour.driver_behaviour import DriverBehaviour
from .point import Point
from .request import Request

@dataclass
class Driver:
    """
    An autonomous driver agent in the simulation.

    A driver can move on the map, accept or reject requests based on its
    behaviour policy, and maintains a history of completed trips for
    statistics and analysis.
    """
    id: int
    position: Point
    speed: float
    behaviour: DriverBehaviour
    status: str = "IDLE"
    current_request: Request | None = None
    history: list = field(default_factory =list)
    position_at_assignment: Point | None = None
    assigned_reward: float = 0.0
    assignment_time: int | None = None
        
    def assign_request(self, request: Request, current_time: int) -> None:
        """
        Assign a delivery request to the driver.

        Records the driver's position at assignment time, sets the current
        request, updates the status to TO_PICKUP, and marks the request
        as assigned.
        """

        self.position_at_assignment = self.position
        self.current_request = request
        self.assigned_reward = 0.0
        self.status = "TO_PICKUP"
        self.assignment_time = current_time
        try:
            request.mark_assigned(self.id)
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Error assigning request to driver {self.id}: {err}")

    @property
    def target_point(self) -> Point | None:
        """
        Get the driver's current target destination.
        
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
        
        return None
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

        destination = self.target_point

        if destination is None:
            return

        try:
            distance = self.position.distance_to(destination)
            movement = self.speed * dt

            if distance <= movement:
                self.position = destination
            else:
                ratio = movement / distance
                direction = destination - self.position
                travel = direction * ratio
                self.position += travel
        except (AttributeError, TypeError, ZeroDivisionError, ValueError) as err:
            print(f"Movement error for driver {self.id}: {err}")
            return

    def complete_pickup(self, time: int) -> None:
        """
        The driver completes the pickup process.

        Updates the driver's status to TO_DROPOFF and marks the current
        request as picked.

        Args:
            time (int): The current simulation time tick.

        Returns:
            None
        """

        if self.current_request and self.status == "TO_PICKUP":
            try:
                self.status = "TO_DROPOFF"
                self.current_request.mark_picked(time)
            except (AttributeError, TypeError, ValueError) as err:
                print(f"Error during pickup completion for driver {self.id}: {err}")
        
    def complete_dropoff(self, time:int) -> None:
        """
        The driver completes the dropoff process.

        Marks the request as delivered, records the trip in history,
        clears the current request and assignment information, and
        updates the driver's status to IDLE.

        Args:
            time (int): The current simulation time tick when dropoff is completed.

        Returns:
            None
        """
        if self.current_request and self.status == "TO_DROPOFF":
            try:
                self.current_request.mark_delivered(time)

                pickup_position = self.current_request.pickup
                dropoff_position = self.current_request.dropoff

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
                    "assignment_time": self.assignment_time,
                    "completion_time": time,
                    "earnings": earnings,
                    "total_distance": total_distance,
                })
            except (AttributeError, TypeError, ValueError) as err:
                print(f"Error during dropoff completion for driver {self.id}: {err}")
            finally:
                self.current_request = None
                self.status = "IDLE"
                self.position_at_assignment = None
                self.assigned_reward = 0.0
                self.assignment_time = None

