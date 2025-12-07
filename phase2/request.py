"""Docstring"""
from point import Point

class Request:
    """Docstring"""

    def __init__(self,
                 id: int,
                 pickup: Point,
                 dropoff: Point,
                 creation_time: int) -> None:
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        self.creation_time = creation_time

        self.status = "WAITING"
        self.assigned_driver_id = None
        self.wait_time = 0

    def is_active(self) -> bool:
        """Docstring"""
        return self.status in ["WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED"]
    
    def mark_assigned(self, driver_id: int) -> None:
        """Docstring"""
        self.status = "ASSIGNED"
        self.assigned_driver_id = driver_id

    def mark_picked(self, t: int) -> None:
        """Docstring"""
        self.status = "PICKED"
        self.wait_time = t - self.creation_time

    def mark_delivered(self, t: int) -> None:
        """Docstring"""
        self.status = "DELIVERED"
        self.wait_time = t - self.creation_time

    def mark_expired(self, t: int) -> None:
        """Docstring"""
        self.status = "EXPIRED"
        self.wait_time = t - self.creation_time

    def update_wait(self, current_time: int) -> None:
        """Docstring"""
        self.wait_time = current_time - self.creation_time

