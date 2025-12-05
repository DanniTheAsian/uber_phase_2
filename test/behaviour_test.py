import unittest
from phase2.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.earning_max_behaviour import EarningMaxBehaviour
from phase2.lazy_behaviour import LazyBehaviour
from .mock.mock_objects import MockDriver, MockRequest, MockOffer, MockPoint


class TestBehaviours(unittest.TestCase):

    def test_greedy_accept(self):
        print("\nRunning test_greedy_accept...")
        driver = MockDriver(1, 0, 0)
        req = MockRequest(1, pickup=MockPoint(3, 4))
        offer = MockOffer(driver, req, travel_time=5, reward=10)

        behaviour = GreedyDistanceBehaviour(max_distance=6)

        try:
            self.assertTrue(behaviour.decide(driver, offer, time=0))
            print("test_greedy_accept: SUCCESSFUL")
        except AssertionError:
            print("test_greedy_accept: FAILED")
            raise

    def test_greedy_reject(self):
        print("\nRunning test_greedy_reject...")
        driver = MockDriver(1, 0, 0)
        req = MockRequest(1, pickup=MockPoint(10, 0))
        offer = MockOffer(driver, req, travel_time=10, reward=10)

        behaviour = GreedyDistanceBehaviour(max_distance=5)

        try:
            self.assertFalse(behaviour.decide(driver, offer, time=0))
            print("test_greedy_reject: SUCCESSFUL")
        except AssertionError:
            print("test_greedy_reject: FAILED")
            raise

    def test_earnings_accept(self):
        print("\nRunning test_earnings_accept...")
        driver = MockDriver()
        req = MockRequest(1)
        offer = MockOffer(driver, req, travel_time=5, reward=20)

        behaviour = EarningMaxBehaviour(min_ratio=3.0)

        try:
            self.assertTrue(behaviour.decide(driver, offer, time=0))
            print("test_earnings_accept: SUCCESSFUL")
        except AssertionError:
            print("test_earnings_accept: FAILED")
            raise

    def test_earnings_reject(self):
        print("\nRunning test_earnings_reject...")
        driver = MockDriver()
        req = MockRequest(1)
        offer = MockOffer(driver, req, travel_time=10, reward=10)

        behaviour = EarningMaxBehaviour(min_ratio=2.0)

        try:
            self.assertFalse(behaviour.decide(driver, offer, time=0))
            print("test_earnings_reject: SUCCESSFUL")
        except AssertionError:
            print("test_earnings_reject: FAILED")
            raise

    def test_lazy_accept(self):
        print("\nRunning test_lazy_accept...")
        driver = MockDriver()
        req = MockRequest(1, wait_time=10)
        offer = MockOffer(driver, req, travel_time=5, reward=10)

        behaviour = LazyBehaviour(max_idle=5)

        try:
            self.assertTrue(behaviour.decide(driver, offer, time=0))
            print("test_lazy_accept: SUCCESSFUL")
        except AssertionError:
            print("test_lazy_accept: FAILED")
            raise

    def test_lazy_reject(self):
        print("\nRunning test_lazy_reject...")
        driver = MockDriver()
        req = MockRequest(1, wait_time=2)
        offer = MockOffer(driver, req, travel_time=5, reward=10)

        behaviour = LazyBehaviour(max_idle=5)

        try:
            self.assertFalse(behaviour.decide(driver, offer, time=0))
            print("test_lazy_reject: SUCCESSFUL")
        except AssertionError:
            print("test_lazy_reject: FAILED")
            raise


if __name__ == "__main__":
    unittest.main()
