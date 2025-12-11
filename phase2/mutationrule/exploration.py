"""
Mutation rule that introduces probabilistic exploration by occasionally
switching a driver's behaviour.
"""

import random
from .mutationrule import MutationRule
from ..behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from ..behaviour.lazy_behaviour import LazyBehaviour
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
        try:
            value = float(probability)
        except (TypeError, ValueError) as err:
            print(f"ExplorationMutationRule init error: {err}")
            value = 0.0

        self.probability = min(1.0, max(0.0, value))

    def maybe_mutate(self, driver: "Driver", time: int) -> None:
        """
        Mutate the driver's behaviour based on an exploration probability.
        The probability slowly increases with time:

            effective_probability = min(1.0, probability * (1 + time * 0.001))

        If the driver currently uses LazyBehaviour, it becomes
        GreedyDistanceBehaviour. Otherwise, it becomes LazyBehaviour.

        Args:
            driver (Driver): The driver that may mutate.
            time (int): Current simulation time.

        Returns:
            None
        """
        try:
            time_value = float(time)
        except (TypeError, ValueError) as err:
            print(f"ExplorationMutationRule time error: {err}")
            return

        effective_probability = self.probability * (1 + time_value * 0.0005)
        effective_probability = min(1.0, max(0.0, effective_probability))

        try:
            roll = random.random()
        except (RuntimeError, ValueError) as err:  # random shouldn't fail, but guard anyway
            print(f"ExplorationMutationRule random error: {err}")
            return

        if roll < effective_probability:
            try:
                behaviour = driver.behaviour
            except AttributeError as err:
                print(f"ExplorationMutationRule behaviour error: {err}")
                return

            if isinstance(behaviour, LazyBehaviour):
                try:
                    driver.behaviour = GreedyDistanceBehaviour(max_distance=10)
                except (AttributeError, TypeError, ValueError) as err:
                    print(f"ExplorationMutationRule switch-to-greedy error: {err}")
            else:
                try:
                    driver.behaviour = LazyBehaviour(max_idle=5)
                except (AttributeError, TypeError, ValueError) as err:
                    print(f"ExplorationMutationRule switch-to-lazy error: {err}")
