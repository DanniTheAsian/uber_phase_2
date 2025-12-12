"""
Abstract base for dispatch policies.

Subclasses implement strategies to propose driver-request assignments for
each simulation tick. The interface expects an `assign` method that returns
a list of (driver, request) pairs.
"""

from abc import ABC,abstractmethod
from ..driver import Driver
from ..request import Request


class DispatchPolicy(ABC):
    """
    Abstract base class representing a dispatch strategy.

    A dispatch policy is responsible for assigning available drivers to
    active requests at each simulation tick. The policy receives the current
    state (drivers, requests, and time) and returns a list of (driver, request)
    assignments.

    Subclasses must implement the `assign` method.
    """
    @abstractmethod
    def assign(self, drivers: list[Driver], requests: list[Request], time: int) -> list[tuple[Driver, Request]]:
        """Return proposed (driver, request) assignments for this tick.

        Args:
            drivers (list[Driver]): The list of available drivers.
            requests (list[Request]): The list of pending requests.
            time (int): The current simulation time. Subclasses may use this to incorporate
                temporal logic, such as prioritizing older requests or idle drivers.

        Returns:
            list[tuple[Driver, Request]]: The assignments chosen by the policy for this tick.
        """
            