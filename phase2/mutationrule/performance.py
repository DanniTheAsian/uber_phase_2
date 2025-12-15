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
    Mutation rule that adjusts a driver's behaviour based on recent activity.

    The rule inspects the driver's trip history and evaluates how active the
    driver has been over the most recent N completed trips. Activity is
    measured as the proportion of completed trips within this window.

    If the driver's average activity level falls below a given threshold,
    the driver mutates and adopts a more greedy distance-based behaviour.

    This models adaptive decision-making, where underperforming drivers become
    less selective in order to increase their chances of receiving future offers.
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
        Evaluate whether the driver should mutate based on recent activity.

        The method considers the last N entries in the driver's trip history.
        If fewer than N trips have been completed, no evaluation is performed.

        Activity is computed as:
            activity = number of recent trips / N

        If the computed activity level is below the configured threshold,
        the driver's behaviour is replaced with a GreedyDistanceBehaviour.

        Args:
            driver (Driver): The driver whose behaviour may be mutated.
            time (int): The current simulation time. Included to satisfy the
                MutationRule interface; not used directly in this rule.

        Returns:
            None

        """
        if len(driver.history) < self.N:
            return

        recent_history = driver.history[-self.N:]

        activity_count = len(recent_history)

        avg_activity = activity_count / self.N

        if avg_activity < self.threshold:
            driver.behaviour = GreedyDistanceBehaviour(max_distance=10)
