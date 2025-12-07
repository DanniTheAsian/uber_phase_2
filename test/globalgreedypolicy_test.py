import unittest

from phase2.policies.global_greedy_policy import GlobalGreedyPolicy
from test.mock.mock_objects import MockDriver, MockRequest, MockPoint


class TestGlobalGreedyPolicy(unittest.TestCase):
    """
    Tests the GlobalGreedyPolicy by verifying that drivers are matched to the
    closest available requests according to the global greedy algorithm.
    Includes tests for both a single-driver scenario and multi-driver scenarios,
    ensuring that matches follow correct distance ordering and no objects are reused.
    """
    def test_single_match(self):
        """
        Tests that a single driver is matched with the closest request.
        """
        print("\nRunning test_single_match...")
        drivers = [
            MockDriver(id=1, x=0, y=0),
        ]
        requests = [
            MockRequest(id=1, pickup=MockPoint(10, 0)),
            MockRequest(id=2, pickup=MockPoint(1, 0)),
        ]

        policy = GlobalGreedyPolicy()
        matches = policy.assign(drivers, requests, time=0)

        try:
            self.assertEqual(len(matches), 1)
            driver, request = matches[0]
            self.assertEqual(driver.id, 1)
            self.assertEqual(request.id, 2)
            print("test_single_match: SUCCESSFUL")
        except AssertionError:
            print("test_single_match: FAILED")
            raise


    def test_multiple_matches(self):
        """
        Tests that multiple drivers are matched with their nearest requests
        according to the global greedy ordering.
        """
        print("\nRunning test_multiple_matches...")
        drivers = [
            MockDriver(id=1, x=0, y=0),
            MockDriver(id=2, x=100, y=100),
        ]

        requests = [
            MockRequest(id=1, pickup=MockPoint(1, 0)),
            MockRequest(id=2, pickup=MockPoint(102, 100)),
        ]

        policy = GlobalGreedyPolicy()
        matches = policy.assign(drivers, requests, time=0)

        matched = {(driver.id, request.id) for driver, request in matches}

        try:
            self.assertIn((1, 1), matched)
            self.assertIn((2, 2), matched)
            self.assertEqual(len(matches), 2)
            print("test_multiple_matches: SUCCESSFUL")
        except AssertionError:
            print("test_multiple_matches: FAILED")
            raise
