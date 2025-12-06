import unittest

from test.mock.mock_objects import MockDriver, MockRequest, MockPoint
from phase2.policies.nearest_neighbor_policy import NearestNeighborPolicy


class TestNearestNeighborPolicy(unittest.TestCase):

    def test_single_match(self):
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
