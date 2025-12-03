import unittest

from mock.mock_objects import MockDriver, MockRequest, MockOffer, MockPoint

from food_delivery.greedy_distance_behaviour import GreedyDistanceBehaviour
from food_delivery.earning_max_behaviour import EarningsMaxBehaviour
from food_delivery.lazy_behaviour import LazyBehaviour

class TestBehaviours(unittest.TestCase):

    def test_greedy_accept(self):
        driver = MockDriver(1, 0, 0)
        req = MockRequest(1, pickup=MockPoint(3, 4))  # distance = 5
        offer = MockOffer(driver, req, travel_time=5, reward=10)

        behaviour = GreedyDistanceBehaviour(max_distance=6)
        self.assertTrue(behaviour.decide(driver, offer, time=0))

    def test_greedy_reject(self):
        driver = MockDriver(1, 0, 0)
        req = MockRequest(1, pickup=MockPoint(10, 0))  # distance = 10
        offer = MockOffer(driver, req, travel_time=10, reward=10)

        behaviour = GreedyDistanceBehaviour(max_distance=5)
        self.assertFalse(behaviour.decide(driver, offer, time=0))

    def test_earnings_accept(self):
        driver = MockDriver()
        req = MockRequest(1)
        offer = MockOffer(driver, req, travel_time=5, reward=20)  # ratio = 4

        behaviour = EarningsMaxBehaviour(min_ratio=3.0)
        self.assertTrue(behaviour.decide(driver, offer, time=0))

    def test_earnings_reject(self):
        driver = MockDriver()
        req = MockRequest(1)
        offer = MockOffer(driver, req, travel_time=10, reward=10)  # ratio = 1

        behaviour = EarningsMaxBehaviour(min_ratio=2.0)
        self.assertFalse(behaviour.decide(driver, offer, time=0))

    def test_lazy_accept(self):
        driver = MockDriver()
        req = MockRequest(1, wait_time=10)
        offer = MockOffer(driver, req, travel_time=5, reward=10)

        behaviour = LazyBehaviour(max_idle=5)
        self.assertTrue(behaviour.decide(driver, offer, time=0))

    def test_lazy_reject(self):
        driver = MockDriver()
        req = MockRequest(1, wait_time=2)
        offer = MockOffer(driver, req, travel_time=5, reward=10)

        behaviour = LazyBehaviour(max_idle=5)
        self.assertFalse(behaviour.decide(driver, offer, time=0))


if __name__ == "__main__":
    unittest.main()