"""
This module contains the Request class, which represents
a single customer order in the delivery simulation.
"""

from phase2.point import Point


class Request:
    """
    Represents a single delivery request in the system.

    It records pickup and dropoff locations, the creation tick, lifecycle
    status (e.g. ``WAITING``, ``ASSIGNED``, ``PICKED``, ``DELIVERED``, ``EXPIRED``),
    the assigned driver, and the total time spent waiting.
    """

    def __init__(
        self,
    id: int,  # noqa: A003
        pickup: Point,
        dropoff: Point,
        creation_time: int,
    ) -> None:
        """
        Create a request with pickup/dropoff points recorded at creation_time.
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
        Return True when the status matches a recognized lifecycle state.
        """
        return self.status in ["WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED"]

    def mark_assigned(self, driver_id: int) -> None:
        """
        Mark the request as assigned and store the provided driver_id.
        """
        self.status = "ASSIGNED"
        self.assigned_driver_id = driver_id

    def mark_picked(self, t: int) -> None:
        """
        Mark the request as picked and capture the wait time at tick t.
        """
        self.status = "PICKED"
        self.wait_time = t - self.creation_time

    def mark_delivered(self, t: int) -> None:
        """
        Mark the request as delivered and freeze the wait time at tick t.
        """
        self.status = "DELIVERED"
        self.wait_time = t - self.creation_time

    def mark_expired(self, t: int) -> None:
        """
        Mark the request as expired after waiting too long at tick t.
        """
        self.status = "EXPIRED"
        self.wait_time = t - self.creation_time

    def update_wait(self, current_time: int) -> None:
        """
        Recalculate wait_time using the provided current_time tick.
        """
        self.wait_time = current_time - self.creation_time