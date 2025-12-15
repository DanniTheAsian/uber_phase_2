"""
Exploration-based mutation rule.

This rule occasionally mutates a driver's behaviour at random, with a
probability that increases slightly over simulation time to encourage
late-stage exploration.
"""

import random
from .mutationrule import MutationRule
from ..behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from ..behaviour.lazy_behaviour import LazyBehaviour
from ..behaviour.earning_max_behaviour import EarningMaxBehaviour
from ..driver import Driver

class ExplorationMutationRule(MutationRule):
    """
    A mutation rule where a driver occasionally switches behaviour.
    The probability increases slightly as the simulation time grows,
    encouraging more exploration later in the simulation.
    """

    def __init__(self, probability: float):
        """
        Initialize the rule with a base mutation probability.

        Args:
            probability (float): Base probability between 0 and 1.

        Example:
            >>> rule = ExplorationMutationRule(0.1)
            >>> rule.probability
            0.1
        """
        self.probability = probability

    def maybe_mutate(self, driver: "Driver", time: int) -> None:
        """
        Mutate the driver's behaviour based on an exploration probability.
        The probability slowly increases with time:

            effective_probability = min(1.0, probability * (1 + time * 0.0005))

        If the driver's behaviour is LazyBehaviour, it becomes GreedyDistanceBehaviour.
        If it's GreedyDistanceBehaviour, it becomes EarningMaxBehaviour.
        Otherwise, it becomes LazyBehaviour.

        Args:
            driver (Driver): The driver that may mutate.
            time (int): Current simulation time.

        Returns:
            None
        """

        if random.random() >= self.probability:
            return

        if isinstance(driver.behaviour, LazyBehaviour):
            driver.behaviour = GreedyDistanceBehaviour(max_distance=10.0)

        elif isinstance(driver.behaviour, GreedyDistanceBehaviour):
            driver.behaviour = EarningMaxBehaviour(min_ratio=1.0)

        else:
            driver.behaviour = LazyBehaviour(max_idle=5)