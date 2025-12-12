"""
Performance-based mutation rule.

This module implements a mutation rule that adjusts a driver's behaviour
based on recent trip performance. If the driver's average served count over
the last N trips is below a threshold, the driver becomes less selective.
"""

from .mutationrule import MutationRule
from ..behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from ..driver import Driver

class PerformanceBasedMutation(MutationRule):
    """
    Mutation rule that adjusts a driver's behaviour based on how many requests
    the driver has successfully served over the last N completed trips.

    The rule inspects the driver's trip history and extracts the number of
    served requests from the most recent N trips. If the driver's average
    performance (measured as served requests per trip) falls below a given
    threshold, the driver mutates and adopts a more greedy behaviour.

    This models adaptive decision-making, where drivers who underperform become
    less selective in order to increase their future opportunities.
    """
   
    def __init__(self, threshold: float, N: int ) -> None:
        """Initialize the mutation rule.

        Args:
            threshold (float): The minimum acceptable average number of served requests across
                the last N trips. If the driver performs below this threshold,
                a mutation will occur.
            N (int): The number of most recent trips to include when evaluating the
                driver's performance window.
        """
        self.threshold = threshold
        self.N = N

    def maybe_mutate(self, driver: Driver, time: int) -> None:
        """
        Evaluate whether the driver should mutate based on recent performance.

        This method examines the last N trip records in the driver's history.
        Each history entry is expected to contain a "served" field indicating
        how many requests the driver served in that completed trip.

        Args:
            driver (Driver): The driver whose behaviour may be mutated.
            time (int): The current simulation time. Included to satisfy the MutationRule
                interface; not directly used in this rule.

        Returns:
            None
        """
        if len(driver.history) < self.N:
            return
        
        served_history = driver.history[-self.N:]

        served_counts = [entry["served"] for entry in served_history]

        avg_served = sum(served_counts) / len(served_counts)

        if avg_served < self.threshold:
            driver.behaviour = GreedyDistanceBehaviour(max_distance=10)