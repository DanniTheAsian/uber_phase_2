"""
This module contains the Request class which represents
a single customer order in the delivery simulation.
"""

from .point import Point


class Request:
    """
    Represents a single delivery request in the system.

    A request keeps track of its pickup and dropoff locations,
    when it was created in the simulation, its current status
    (e.g. WAITING, ASSIGNED, PICKED, DELIVERED, EXPIRED),
    which driver is assigned to it, and how long it
    has been waiting in total.
    """

    def __init__(
        self,
        id: int,
        pickup: Point,
        dropoff: Point,
        creation_time: int,
    ) -> None:
        """
        Initialize a Request instance.

        Args:
            id (int): Unique identifier for the request.
            pickup (Point): Pickup location on the map.
            dropoff (Point): Dropoff location on the map.
            creation_time (int): Simulation time tick when the request was created.

        Returns:
            None
        """
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        self.creation_time = creation_time

        self.status = "WAITING"
        self.assigned_driver_id: int | None = None
        self.wait_time: int = 0

    def is_active(self) -> bool:
        """
        
        Check whether the request is in a valid lifecycle state.

        Returns:
            bool: True if the status is a known state, False otherwise.
        """
        return self.status in ["WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED"]

    def mark_assigned(self, driver_id: int) -> None:
        """
        Mark the request as assigned to a driver.

        Updates the status to ASSIGNED and stores the id of the driver
        that has been chosen to handle this request.

        Args:
            driver_id (int): The id of the assigned driver.

        Returns:
            None
        """
        try:
            self.status = "ASSIGNED"
            self.assigned_driver_id = driver_id
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Error in mark_assigned: {err}")

    def mark_picked(self, t: int) -> None:
        """
        Mark the request as picked up by the driver.

        Updates the status to PICKED and sets the waiting time to the
        time elapsed since creation.

        Args:
            t (int): Current simulation time tick when pickup happens.

        Returns:
            None
        """
        try:
            self.status = "PICKED"
            self.wait_time = t - self.creation_time
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Error in mark_picked: {err}")

    def mark_delivered(self, t: int) -> None:
        """
        Mark the request as delivered to the customer.

        Updates the status to DELIVERED and sets the waiting time to the
        total time from creation until delivery.

        Args:
            t (int): Current simulation time tick when delivery happens.

        Returns:
            None
        """
        try:
            self.status = "DELIVERED"
            self.wait_time = t - self.creation_time
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Error in mark_delivered: {err}")

    def mark_expired(self, t: int) -> None:
        """
        Mark the request as expired.

        Used when the request has waited too long without being
        completed. Updates the status to EXPIRED and sets the
        waiting time to the elapsed time since creation.

        Args:
            t (int): Current simulation time tick when the request expires.

        Returns:
            None
        """
        try:
            self.status = "EXPIRED"
            self.wait_time = t - self.creation_time
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Error in mark_expired: {err}")

    def update_wait(self, current_time: int) -> None:
        """
        Recalculate the waiting time based on the current simulation time.

        Args:
            current_time (int): Current simulation time tick.

        Returns:
            None
        """
        try:
            self.wait_time = current_time - self.creation_time
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Error updating wait_time: {err}")