"""
Performance-based mutation rule.

This mutation rule adjusts a driver's behaviour based on recent economic
performance. If the average earning over the most recent trips falls below
a specified threshold, the driver becomes less selective in order to
improve future performance.
"""


from .mutationrule import MutationRule
from ..behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from ..driver import Driver

class PerformanceBasedMutation(MutationRule):
    """
    Mutation rule that changes a driver's behaviour when recent earnings
    indicate poor performance.

    If the average earning over the last N completed trips is below a
    configurable threshold, the driver switches to a less selective behaviour.
    """
    def __init__(self, min_avg_earnings: float = 60.0, N: int = 5) -> None:
        """
        Initialize the mutation rule.

        Args:
            min_avg_earnings (float): Minimum acceptable average earning.
            N (int): Number of recent trips used to evaluate performance.
        """
        self.min_avg_earnings = min_avg_earnings
        self.N = N

    def maybe_mutate(self, driver: Driver, time: int) -> None:
        """
        Evaluate recent trips and mutate behaviour if performance is poor.

        The method computes the average earning over the driver's most recent
        N completed trips. If this average falls below the configured threshold,
        the driver's behaviour is changed to a less selective strategy.
        """
        # Not enough history yet
        if len(driver.history) < self.N:
            return

        recent_trips = []
        # Look at the last N trips (simple and explicit)
        for i in range(self.N):
            recent_trips.append(driver.history[-1 - i])

        avg_earnings = sum(trip["earnings"] for trip in recent_trips) / self.N



        if avg_earnings < self.min_avg_earnings:
            driver.behaviour = GreedyDistanceBehaviour(max_distance=10.0)



        #print(
        #    f"[MutationCheck] Driver {driver.id} | "
        #    f"Avg earnings (last {self.N} trips): {avg_earnings:.2f} | "
        #    f"Threshold: {self.min_avg_earnings}"
        #)