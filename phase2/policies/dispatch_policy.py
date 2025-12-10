"""
Abstract base for dispatch policies that assign drivers to requests.
"""
from abc import ABC, abstractmethod
from ..driver import Driver
from ..request import Request


class DispatchPolicy(ABC):
    """
    Assign available drivers to active requests at each simulation tick.

    Subclasses must supply the ``assign`` method that proposes pairings.
    """

    @abstractmethod
    def assign(self, drivers: list[Driver], requests: list[Request], time: int) -> list[tuple[Driver, Request]]:
        """
        Return proposed (driver, request) assignments for this tick.

        Args:
            drivers (list[Driver]): Available drivers that can be assigned.
            requests (list[Request]): Pending requests awaiting dispatch.
            time (int): Current simulation tick provided for policy context.

        Returns:
            list[tuple[Driver, Request]]: Proposed assignments for this tick.
        """
        raise NotImplementedError
