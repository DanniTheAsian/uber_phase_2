import unittest
from phase2.mutationrule.performance import PerformanceBasedMutation
from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.behaviour.lazy_behaviour import LazyBehaviour
from test.mock.mock_objects import MockDriver


class TestPerformanceBasedMutation(unittest.TestCase):
    """
    Tests included:
    1. test_mutation_occurs:
       - Ensures that mutation happens when the driver's average served
         value is below the threshold.

    2. test_no_mutation_when_high_performance:
       - Ensures that no mutation happens when the driver's performance
         meets or exceeds the threshold. The behaviour object must remain
         identical.

    3. test_not_enough_trips:
       - Ensures that no mutation occurs when the driver has fewer than N
         historical trip entries. The rule requires sufficient data to
         calculate an average.
    """
    """
    def test_mutation_occurs(self):
        """
        Mutation should occur when avg served < threshold.
        """
        print("\nRunning test_mutation_occurs...")

        driver = MockDriver(
            behaviour=LazyBehaviour(None),
            history=[
                {"served": 0}, {"served": 0}, {"served": 1}
            ]
        )

        rule = PerformanceBasedMutation(threshold=1.0, N=3)
        rule.maybe_mutate(driver, time=0)

        try:
            self.assertIsInstance(driver.behaviour, GreedyDistanceBehaviour)
            print("test_mutation_occurs: SUCCESSFUL")
        except AssertionError:
            print("test_mutation_occurs: FAILED")
            raise


    def test_no_mutation_when_high_performance(self):
        """
        No mutation should occur when avg served >= threshold.
        """
        print("\nRunning test_no_mutation_when_high_performance...")

        original_behaviour = LazyBehaviour(None)

        driver = MockDriver(
            behaviour=original_behaviour,
            history=[
                {"served": 1}, {"served": 1}, {"served": 1}
            ]
        )

        rule = PerformanceBasedMutation(threshold=0.5, N=3)
        rule.maybe_mutate(driver, time=0)

        try:
            self.assertIs(driver.behaviour, original_behaviour)
            print("test_no_mutation_when_high_performance: SUCCESSFUL")
        except AssertionError:
            print("test_no_mutation_when_high_performance: FAILED")
            raise


    def test_not_enough_trips(self):
        """
        No mutation should occur if history contains fewer than N trips.
        """
        print("\nRunning test_not_enough_trips...")

        original_behaviour = LazyBehaviour(None)

        driver = MockDriver(
            behaviour=original_behaviour,
            history=[
                {"served": 1}
            ]
        )

        rule = PerformanceBasedMutation(threshold=1.0, N=3)
        rule.maybe_mutate(driver, time=0)

        try:
            self.assertIs(driver.behaviour, original_behaviour)
            print("test_not_enough_trips: SUCCESSFUL")
        except AssertionError:
            print("test_not_enough_trips: FAILED")
            raise
