"""
This module contains the Request class, which represents
a single customer order in the delivery simulation.
"""

from .point import Point


class Request:
    """
    Represents a single delivery request in the system.

    It records pickup and dropoff locations, the creation tick, lifecycle
    status (e.g. ``WAITING``, ``ASSIGNED``, ``PICKED``, ``DELIVERED``, ``EXPIRED``),
    the assigned driver, and the total time spent waiting.
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
        try:
            self.id = int(id)
        except (TypeError, ValueError) as err:
            print(f"Request init id error: {err}")
            self.id = -1

        self.pickup = pickup if isinstance(pickup, Point) else None
        if self.pickup is None:
            print("Request init pickup error: invalid Point")

        self.dropoff = dropoff if isinstance(dropoff, Point) else None
        if self.dropoff is None:
            print("Request init dropoff error: invalid Point")

        try:
            self.creation_time = int(creation_time)
        except (TypeError, ValueError) as err:
            print(f"Request init creation time error: {err}")
            self.creation_time = 0

        self.status = "WAITING"
        self.assigned_driver_id: int | None = None
        self.wait_time: int = 0

    def is_active(self) -> bool:
        """
        Check that the request status is one of the recognized lifecycle states.

        Returns:
            bool: True if the status matches WAITING/ASSIGNED/PICKED/DELIVERED/EXPIRED.
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
            self.assigned_driver_id = int(driver_id)
        except (TypeError, ValueError) as err:
            print(f"Request mark_assigned error: {err}")
            self.status = "ASSIGNED"
            self.assigned_driver_id = None

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
        self.status = "PICKED"
        try:
            self.wait_time = int(t) - self.creation_time
        except (TypeError, ValueError) as err:
            print(f"Request mark_picked error: {err}")
            self.wait_time = 0

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
        self.status = "DELIVERED"
        try:
            self.wait_time = int(t) - self.creation_time
        except (TypeError, ValueError) as err:
            print(f"Request mark_delivered error: {err}")
            self.wait_time = 0

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
        self.status = "EXPIRED"
        try:
            self.wait_time = int(t) - self.creation_time
        except (TypeError, ValueError) as err:
            print(f"Request mark_expired error: {err}")
            self.wait_time = 0

    def update_wait(self, current_time: int) -> None:
        """
        Recalculate the waiting time based on the current simulation time.

        Args:
            current_time (int): Current simulation time tick.

        Returns:
            None
        """
        try:
            self.wait_time = int(current_time) - self.creation_time
        except (TypeError, ValueError) as err:
            print(f"Request update_wait error: {err}")
            self.wait_time = 0