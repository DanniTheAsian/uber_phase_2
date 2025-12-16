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
    Mutation rule that adapts a driver's behaviour based on recent results.

    The rule examines the driver's most recent N trips and measures performance
    as the proportion of trips that were successfully delivered.

    If this success rate falls below a configured threshold, the driver mutates
    and adopts a greedy distance-based behaviour.
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

        The method considers the last N entries in the driver's trip history.
        If fewer than N trips have been completed, no evaluation is performed.

        Performance is computed as:
            success_rate = delivered_trips / N

        If the success rate is below the configured threshold, the driver's behaviour
        is replaced with a GreedyDistanceBehaviour.

        Args:
            driver (Driver): The driver whose behaviour may be mutated.
            time (int): Current simulation time (not used in this rule).

        Returns:
            None
        """

        if len(driver.history) < self.N:
            return

        recent_trips = driver.history[-self.N:]

        delivered = 0
        for trip in recent_trips:
            if trip.get("status") == "DELIVERED":
                delivered += 1

        success_rate = delivered / self.N

        if success_rate < self.threshold:
            driver.behaviour = GreedyDistanceBehaviour(max_distance=10.0)
