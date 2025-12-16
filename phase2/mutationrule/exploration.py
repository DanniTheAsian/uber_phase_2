"""
Exploration-based mutation rule.

This rule randomly mutates a driver's behaviour with a fixed probability
in order to encourage exploration.
"""
import random
from .mutationrule import MutationRule
from ..behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from ..behaviour.lazy_behaviour import LazyBehaviour
from ..behaviour.earning_max_behaviour import EarningMaxBehaviour
from ..driver import Driver

class ExplorationMutationRule(MutationRule):
    """
    A mutation rule where a driver occasionally switches behaviour
    at random to avoid static behaviour.
    """

    def __init__(self, probability: float):
        """
        Initialize the rule with a base mutation probability.

        Args:
            probability (float): Base mutation probability between 0 and 1.

        Example:
            >>> rule = ExplorationMutationRule(0.1)
            >>> rule.probability
            0.1
        """
        self.probability = probability

    def maybe_mutate(self, driver: "Driver", time: int) -> None:
        """
        Randomly mutate the driver's behaviour.
        
        Behaviour transitions follow a simple cycle:
        - LazyBehaviour -> GreedyDistanceBehaviour
        - GreedyDistanceBehaviour -> EarningMaxBehaviour
        - Otherwise -> LazyBehaviour

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
            driver.behaviour = LazyBehaviour(min_wait_time=5)