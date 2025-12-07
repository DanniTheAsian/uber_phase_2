import unittest
from unittest.mock import patch

from phase2.mutationrule.exploration import ExplorationMutationRule
from phase2.behaviour.lazy_behaviour import LazyBehaviour
from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from test.mock.mock_objects import MockDriver


class TestExplorationMutationRule(unittest.TestCase):
    """
    Unit tests for the ExplorationMutationRule.

    Scenarios tested:
    1. Mutation occurs when random.random() < effective probability.
    2. No mutation occurs when random.random() >= effective probability.
    3. Behaviour switches correctly between Lazy and Greedy.
    """

    @patch("random.random", return_value=0.0)
    def test_mutation_occurs_lazy_to_greedy(self, mock_random):
        """
        If the driver is LazyBehaviour and probability is triggered,
        behaviour should mutate into GreedyDistanceBehaviour.
        """
        driver = MockDriver(behaviour=LazyBehaviour(max_idle=5))

        rule = ExplorationMutationRule(probability=0.1)
        rule.maybe_mutate(driver, time=100)

        self.assertIsInstance(driver.behaviour, GreedyDistanceBehaviour)


    @patch("random.random", return_value=0.0)
    def test_mutation_occurs_greedy_to_lazy(self, mock_random):
        """
        If the driver is GreedyBehaviour and probability is triggered,
        behaviour should mutate into LazyBehaviour.
        """
        driver = MockDriver(behaviour=GreedyDistanceBehaviour(max_distance=10))

        rule = ExplorationMutationRule(probability=0.1)
        rule.maybe_mutate(driver, time=100)

        self.assertIsInstance(driver.behaviour, LazyBehaviour)


    @patch("random.random", return_value=1.0)
    def test_no_mutation_when_probability_not_met(self, mock_random):
        """
        No mutation should occur if random.random() >= effective probability.
        Behaviour must remain unchanged.
        """
        original_behaviour = LazyBehaviour(max_idle=5)
        driver = MockDriver(behaviour=original_behaviour)

        rule = ExplorationMutationRule(probability=0.1)
        rule.maybe_mutate(driver, time=100)

        self.assertIs(driver.behaviour, original_behaviour)


if __name__ == "__main__":
    unittest.main()
