import unittest

from test.mock.mock_objects import MockDriver, MockRequest, MockPoint
from phase2.policies.nearest_neighbor_policy import NearestNeighborPolicy


class TestNearestNeighborPolicy(unittest.TestCase):
    """
    Unit tests for the NearestNeighborPolicy, verifying that the policy matches
    drivers and requests using a stepwise nearest-neighbor greedy selection.
    The tests cover simple scenarios, multi-step greedy behavior, and conflict
    situations where multiple matches are possible.
    """
    def test_single_match(self):
        """
        Tests that a single driver is correctly matched with the only available request.

        This test validates the simplest scenario: one driver and one request at
        a known distance. The NearestNeighborPolicy should always return exactly
        one match, pairing the driver with the request. This verifies the correct
        handling of minimal input and proper output structure.
        """
        print("\nRunning test_single_match...")
        drivers = [
            MockDriver(id=1, x=0, y=0),
        ]
        requests = [
            MockRequest(id=1, pickup=MockPoint(5, 5)),
        ]

        policy = NearestNeighborPolicy()
        matches = policy.assign(drivers, requests, time=0)

        try:
            self.assertEqual(len(matches), 1)
            d, r = matches[0]
            self.assertEqual(d.id, 1)
            self.assertEqual(r.id, 1)
            print("test_single_match: SUCCESSFUL")
        except AssertionError:
            print("test_single_match: FAILED")
            raise


    def test_greedy_stepwise_selection(self):
        """
        Tests the greedy step-by-step selection used by NearestNeighborPolicy.

        This test sets up two drivers and two requests such that each driver has
        one uniquely closest request. The algorithm should:
        1. First match Driver 1 to Request 1 (closest pair).
        2. Remove both from further consideration.
        3. Match Driver 2 to Request 2 in the next iteration.

        """
        print("\nRunning test_greedy_stepwise_selection...")
        drivers = [
            MockDriver(id=1, x=0, y=0),
            MockDriver(id=2, x=100, y=100),
        ]
        requests = [
            MockRequest(id=1, pickup=MockPoint(1, 1)),       # Nær D1
            MockRequest(id=2, pickup=MockPoint(101, 100)),   # Nær D2
        ]

        policy = NearestNeighborPolicy()
        matches = policy.assign(drivers, requests, time=0)

        matched = {(d.id, r.id) for d, r in matches}

        try:
            self.assertIn((1, 1), matched)
            self.assertIn((2, 2), matched)
            self.assertEqual(len(matches), 2)
            print("test_greedy_stepwise_selection: SUCCESSFUL")
        except AssertionError:
            print("test_greedy_stepwise_selection: FAILED")
            raise


    def test_conflicting_choices(self):

        """
        Tests behavior when two drivers compete for a request, ensuring
        nearest-neighbor logic is respected.

        One request is placed close to Driver 1 and far from Driver 2.
        The expected greedy behavior is:

        - Driver 1 should be matched to Request 1 (the closest match),
          even though Driver 2 is also technically available.

        This test ensures that the algorithm resolves conflicts correctly
        by always prioritizing the smallest distance in each iteration.
        """
        print("\nRunning test_conflicting_choices...")
        drivers = [
            MockDriver(id=1, x=0, y=0),
            MockDriver(id=2, x=2, y=0),
        ]
        requests = [
            MockRequest(id=1, pickup=MockPoint(1, 0)),   # nær D1
            MockRequest(id=2, pickup=MockPoint(100, 0)), # langt væk
        ]

        policy = NearestNeighborPolicy()
        matches = policy.assign(drivers, requests, time=0)

        try:
            d1, r1 = matches[0]
            self.assertEqual(d1.id, 1)
            self.assertEqual(r1.id, 1)
            print("test_conflicting_choices: SUCCESSFUL")
        except AssertionError:
            print("test_conflicting_choices: FAILED")
            raise
