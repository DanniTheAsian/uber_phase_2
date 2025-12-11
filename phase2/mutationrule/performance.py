"""
Mutation rule that adapts driver behaviour based on recent performance.
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
   
    def __init__(self, threshold: float, N: int) -> None:
        """
        Initialize the mutation rule.

        Args:
            threshold (float): The minimum acceptable average number of served requests across
                the last N trips. If the driver performs below this threshold,
                a mutation will occurs.
            N (int): Number of most recent trips used to evaluate performance.
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
            time (int): The current simulation time. Included to satisfy the
                MutationRule interface; not directly used in this rule.

        Returns:
            None
        """
        try:
            history = driver.history
        except AttributeError as err:
            print(f"PerformanceBasedMutation history error: {err}")
            return

        try:
            history_len = len(history)
        except TypeError as err:
            print(f"PerformanceBasedMutation history length error: {err}")
            return

        try:
            window = int(self.N)
        except (TypeError, ValueError) as err:
            print(f"PerformanceBasedMutation window error: {err}")
            return

        if history_len < window or window <= 0:
            return
        
        try:
            served_history = history[-window:]
        except TypeError as err:
            print(f"PerformanceBasedMutation slice error: {err}")
            return

        served_counts: list[float] = []
        for entry in served_history:
            try:
                served_value = entry["served"]
            except (TypeError, KeyError) as err:
                print(f"PerformanceBasedMutation entry error: {err}")
                continue

            try:
                served_counts.append(float(served_value))
            except (TypeError, ValueError) as err:
                print(f"PerformanceBasedMutation served value error: {err}")
                continue

        if not served_counts:
            return

        avg_served = sum(served_counts) / len(served_counts)

        try:
            threshold_value = float(self.threshold)
        except (TypeError, ValueError) as err:
            print(f"PerformanceBasedMutation threshold error: {err}")
            return

        if avg_served < threshold_value:
            try:
                driver.behaviour = GreedyDistanceBehaviour(max_distance=10)
            except (AttributeError, TypeError, ValueError) as err:
                print(f"PerformanceBasedMutation mutation error: {err}")