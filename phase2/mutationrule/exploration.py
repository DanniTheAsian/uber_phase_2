from phase2.mutationrule.mutationrule import MutationRule
from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.behaviour.lazy_behaviour import LazyBehaviour
import random

class ExplorationMutationRule(MutationRule):

    def __init__(self, probability):
        self.probability = probability

    def maybe_mutate(self, driver, time:int) -> None:
        if random.random() < self.probability:

            if isinstance(driver.behaviour, LazyBehaviour):
                driver.behaviour = GreedyDistanceBehaviour(max_distance=10)
            else:
                driver.behaviour = LazyBehaviour
            