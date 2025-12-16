"""
Abstract base class for dispatch policies.

A dispatch policy defines how drivers are matched with requests at each
simulation tick. Concrete policies implement different strategies for
selecting which driver should serve which request.
"""

from abc import ABC,abstractmethod
from ..driver import Driver
from ..request import Request


class DispatchPolicy(ABC):
    """
    Abstract base class representing a dispatch strategy.

    A dispatch policy is responsible for proposing assignments between
    available drivers and active requests at a given simulation time.
    The policy does not execute the assignment itself, but returns a list
    of proposed (driver, request) pairs to be evaluated by the simulation.
    """
    @abstractmethod
    def assign(self, drivers: list[Driver], requests: list[Request], time: int) -> list[tuple[Driver, Request]]:
        """
        Propose driver–request assignments for the current simulation tick.

        The method receives the current list of drivers and pending requests
        and returns a list of proposed (driver, request) pairs. Each driver
        and request should appear at most once in the returned list.

        Args:
            drivers (list[Driver]): Available drivers at the current tick.
            requests (list[Request]): Pending requests waiting to be assigned.
            time (int): Current simulation time. Can be used to incorporate
                time-dependent logic, such as prioritizing older requests.

        Returns:
            list[tuple[Driver, Request]]: Proposed driver–request assignments.
        """