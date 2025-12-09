import unittest
from unittest.mock import Mock
from phase2.offer import Offer
from phase2.driver import Driver
from phase2.request import Request
from phase2.point import Point


class TestOffer(unittest.TestCase):
    """Test suite for the Offer class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock driver
        self.driver = Mock(spec=Driver)
        self.driver.id = 1
        self.driver.position = Point(0, 0)
        self.driver.status = "AVAILABLE"

        # Create mock request
        self.request = Mock(spec=Request)
        self.request.id = 1
        self.request.pickup = Point(10, 10)
        self.request.dropoff = Point(20, 20)
        self.request.status = "WAITING"

        # Create offer with required parameters
        self.offer = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5
        )

    def test_offer_initialization_basic(self):
        """Test that an Offer initializes with required parameters."""
        self.assertEqual(self.offer.driver, self.driver)
        self.assertEqual(self.offer.request, self.request)
        self.assertEqual(self.offer.estimated_travel_time, 5.5)
        self.assertIsNone(self.offer.estimated_reward)

    def test_offer_initialization_with_reward(self):
        """Test that an Offer initializes with optional reward parameter."""
        offer_with_reward = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5,
            estimated_reward=10.0
        )
        self.assertEqual(offer_with_reward.estimated_reward, 10.0)

    def test_offer_driver_assignment(self):
        """Test that the driver is correctly assigned to the offer."""
        self.assertIs(self.offer.driver, self.driver)

    def test_offer_request_assignment(self):
        """Test that the request is correctly assigned to the offer."""
        self.assertIs(self.offer.request, self.request)

    def test_offer_estimated_travel_time_positive(self):
        """Test offer with positive estimated travel time."""
        self.assertGreater(self.offer.estimated_travel_time, 0)
        self.assertEqual(self.offer.estimated_travel_time, 5.5)

    def test_offer_estimated_travel_time_zero(self):
        """Test offer with zero estimated travel time."""
        offer_zero_time = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=0
        )
        self.assertEqual(offer_zero_time.estimated_travel_time, 0)

    def test_offer_estimated_travel_time_large_value(self):
        """Test offer with large estimated travel time."""
        offer_large_time = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=1000.5
        )
        self.assertEqual(offer_large_time.estimated_travel_time, 1000.5)

    def test_offer_estimated_reward_positive(self):
        """Test offer with positive estimated reward."""
        offer_reward = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5,
            estimated_reward=15.75
        )
        self.assertGreater(offer_reward.estimated_reward, 0)
        self.assertEqual(offer_reward.estimated_reward, 15.75)

    def test_offer_estimated_reward_zero(self):
        """Test offer with zero estimated reward."""
        offer_zero_reward = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5,
            estimated_reward=0
        )
        self.assertEqual(offer_zero_reward.estimated_reward, 0)

    def test_offer_estimated_reward_none_by_default(self):
        """Test that estimated reward defaults to None when not provided."""
        self.assertIsNone(self.offer.estimated_reward)

    def test_offer_with_different_drivers(self):
        """Test creating offers for different drivers."""
        driver2 = Mock(spec=Driver)
        driver2.id = 2

        offer1 = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5
        )
        offer2 = Offer(
            driver=driver2,
            request=self.request,
            estimated_travel_time=7.5
        )

        self.assertNotEqual(offer1.driver, offer2.driver)
        self.assertEqual(offer1.driver.id, 1)
        self.assertEqual(offer2.driver.id, 2)

    def test_offer_with_different_requests(self):
        """Test creating offers for different requests."""
        request2 = Mock(spec=Request)
        request2.id = 2

        offer1 = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5
        )
        offer2 = Offer(
            driver=self.driver,
            request=request2,
            estimated_travel_time=5.5
        )

        self.assertNotEqual(offer1.request, offer2.request)
        self.assertEqual(offer1.request.id, 1)
        self.assertEqual(offer2.request.id, 2)

    def test_offer_multiple_offers_same_request(self):
        """Test multiple offers for the same request from different drivers."""
        driver2 = Mock(spec=Driver)
        driver2.id = 2

        offer1 = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5,
            estimated_reward=10.0
        )
        offer2 = Offer(
            driver=driver2,
            request=self.request,
            estimated_travel_time=8.5,
            estimated_reward=15.0
        )

        # Both offers reference the same request but different drivers
        self.assertEqual(offer1.request, offer2.request)
        self.assertNotEqual(offer1.driver, offer2.driver)
        self.assertLess(offer1.estimated_travel_time, offer2.estimated_travel_time)

    def test_offer_multiple_offers_same_driver(self):
        """Test multiple offers to the same driver for different requests."""
        request2 = Mock(spec=Request)
        request2.id = 2

        offer1 = Offer(
            driver=self.driver,
            request=self.request,
            estimated_travel_time=5.5,
            estimated_reward=10.0
        )
        offer2 = Offer(
            driver=self.driver,
            request=request2,
            estimated_travel_time=8.5,
            estimated_reward=15.0
        )

        # Both offers to the same driver but different requests
        self.assertEqual(offer1.driver, offer2.driver)
        self.assertNotEqual(offer1.request, offer2.request)

    def test_offer_attributes_are_mutable(self):
        """Test that offer attributes can be read (immutability not enforced)."""
        # Verify we can access and read attributes
        self.assertEqual(self.offer.driver, self.driver)
        self.assertEqual(self.offer.request, self.request)
        self.assertEqual(self.offer.estimated_travel_time, 5.5)
        self.assertIsNone(self.offer.estimated_reward)

    def test_offer_with_float_travel_time(self):
        """Test offer with various float values for travel time."""
        test_times = [0.1, 1.5, 3.14159, 999.9999]
        
        for test_time in test_times:
            offer = Offer(
                driver=self.driver,
                request=self.request,
                estimated_travel_time=test_time
            )
            self.assertEqual(offer.estimated_travel_time, test_time)

    def test_offer_with_float_reward(self):
        """Test offer with various float values for reward."""
        test_rewards = [0.1, 1.5, 3.14159, 999.9999]
        
        for test_reward in test_rewards:
            offer = Offer(
                driver=self.driver,
                request=self.request,
                estimated_travel_time=5.5,
                estimated_reward=test_reward
            )
            self.assertEqual(offer.estimated_reward, test_reward)

    def test_offer_docstring_exists(self):
        """Test that the Offer class has proper documentation."""
        self.assertIsNotNone(Offer.__doc__)
        self.assertTrue(len(Offer.__doc__) > 0)

    def test_offer_init_docstring_exists(self):
        """Test that the __init__ method has proper documentation."""
        self.assertIsNotNone(Offer.__init__.__doc__)
        self.assertTrue(len(Offer.__init__.__doc__) > 0)


if __name__ == '__main__':
    unittest.main()
