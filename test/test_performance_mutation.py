import unittest
from phase2.mutationrule.performance import PerformanceBasedMutation
from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.behaviour.lazy_behaviour import LazyBehaviour
from test.mock.mock_objects import MockDriver


class TestPerformanceBasedMutation(unittest.TestCase):
    """
    Tests for PerformanceBasedMutation.

    The mutation rule evaluates activity based on the number
    of recent history entries relative to N.
    """

    def test_mutates_when_activity_below_threshold(self):
        """
        Mutation should occur when avg_activity < threshold.

        avg_activity = len(history) / N = 1.0
        threshold > 1.0  -> mutation
        """
        driver = MockDriver(
            behaviour=LazyBehaviour(None),
            history=[
                {"served": 0},
                {"served": 1},
                {"served": 0},
            ]
        )

        rule = PerformanceBasedMutation(threshold=1.1, N=3)
        rule.maybe_mutate(driver, time=0)

        self.assertIsInstance(
            driver.behaviour,
            GreedyDistanceBehaviour
        )

    def test_no_mutation_when_activity_meets_threshold(self):
        """
        No mutation should occur when avg_activity >= threshold.
        """
        original_behaviour = LazyBehaviour(None)

        driver = MockDriver(
            behaviour=original_behaviour,
            history=[
                {"served": 1},
                {"served": 1},
                {"served": 1},
            ]
        )

        rule = PerformanceBasedMutation(threshold=1.0, N=3)
        rule.maybe_mutate(driver, time=0)

        self.assertIs(
            driver.behaviour,
            original_behaviour
        )

    def test_no_mutation_when_not_enough_history(self):
        """
        No mutation should occur if history contains fewer than N entries.
        """
        original_behaviour = LazyBehaviour(None)

        driver = MockDriver(
            behaviour=original_behaviour,
            history=[
                {"served": 0},
            ]
        )

        rule = PerformanceBasedMutation(threshold=1.5, N=3)
        rule.maybe_mutate(driver, time=0)

        self.assertIs(
            driver.behaviour,
            original_behaviour
        )
