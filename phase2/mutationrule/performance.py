"""
Performance-based mutation rule.

This mutation rule adjusts a driver's behaviour based on recent performance.
If a driver delivers too few of its most recent trips, it becomes less
selective in order to improve future performance.
"""


from .mutationrule import MutationRule
from ..behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from ..driver import Driver

class PerformanceBasedMutation(MutationRule):
    """
    Mutation rule that changes a driver's behaviour when recent performance is poor.

    If a driver delivers too few of its most recent trips, the driver switches
    to a less selective behaviour.
    """

    def __init__(self, min_avg_earnings: float, N: int) -> None:
        """
        Initialize the mutation rule.

        Args:
            threshold (float): Minimum acceptable success rate (0–1).
            N (int): Number of recent trips used to evaluate performance.
        """
        self.min_avg_earnings = min_avg_earnings
        self.N = N

    def maybe_mutate(self, driver: Driver, time: int) -> None:
        """
        Evaluate recent trips and mutate behaviour if performance is low.

        The method checks the driver's most recent N trips. If the proportion
        of delivered trips is below the configured threshold, the driver's
        behaviour is changed.
        """
        # Not enough history yet
        if len(driver.history) < self.N:
            return

        recent_trips = []
        # Look at the last N trips (simple and explicit)
        for i in range(self.N):
            recent_trips.append(driver.history[-1 - i])

        avg_earnings = sum(trip["earnings"] for trip in recent_trips) / self.N

        if avg_earnings< self.min_avg_earnings:
            driver.behaviour = GreedyDistanceBehaviour(max_distance=10.0)

