"""
Defines the abstract base class for mutation rules.

A mutation rule controls whether a driver's behaviour should change
during the simulation. Different rules can implement their own logic,
such as performance-based mutation or random exploration.
"""

from abc import ABC, abstractmethod
from ..driver import Driver

class MutationRule(ABC):
    """
    Abstract base class for all mutation rule types.

    A mutation rule decides if and when a driver should switch to
    another behaviour. This allows dynamic behaviour changes during
    the simulation.
    """
    @abstractmethod
    def maybe_mutate(self, driver: Driver, time: int) -> None:
        """
        Decide whether the driver should mutate to another behaviour.

        Arguments:
            driver (Driver): The driver that may mutate.
            time (int): Current simulation time.

        Returns:
            None
        """