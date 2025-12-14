import unittest
from phase2.request import Request
from phase2.point import Point


class TestRequest(unittest.TestCase):
    """Test suite for the Request class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.pickup = Point(0, 0)
        self.dropoff = Point(10, 10)
        self.request = Request(
            id=1,
            pickup=self.pickup,
            dropoff=self.dropoff,
            creation_time=0
        )

    def test_request_initialization(self):
        """Test that a Request is initialized correctly."""
        self.assertEqual(self.request.id, 1)
        self.assertEqual(self.request.pickup, self.pickup)
        self.assertEqual(self.request.dropoff, self.dropoff)
        self.assertEqual(self.request.creation_time, 0)
        self.assertEqual(self.request.status, "WAITING")
        self.assertIsNone(self.request.assigned_driver_id)
        self.assertEqual(self.request.wait_time, 0)

    def test_is_active_waiting(self):
        """Test is_active returns True for WAITING status."""
        self.request.status = "WAITING"
        self.assertTrue(self.request.is_active())

    def test_is_active_assigned(self):
        """Test is_active returns True for ASSIGNED status."""
        self.request.status = "ASSIGNED"
        self.assertTrue(self.request.is_active())

    def test_is_active_picked(self):
        """Test is_active returns True for PICKED status."""
        self.request.status = "PICKED"
        self.assertTrue(self.request.is_active())

    def test_is_active_delivered(self):
        """Test is_active returns True for DELIVERED status."""
        self.request.status = "DELIVERED"
        self.assertTrue(self.request.is_active())

    def test_is_active_expired(self):
        """Test is_active returns True for EXPIRED status."""
        self.request.status = "EXPIRED"
        self.assertTrue(self.request.is_active())

    def test_is_active_unknown_status(self):
        """Test is_active returns False for unknown status."""
        self.request.status = "UNKNOWN"
        self.assertFalse(self.request.is_active())

    def test_mark_assigned(self):
        """Test that mark_assigned updates status and driver_id."""
        driver_id = 42
        self.request.mark_assigned(driver_id)
        self.assertEqual(self.request.status, "ASSIGNED")
        self.assertEqual(self.request.assigned_driver_id, driver_id)

    def test_mark_picked(self):
        """Test that mark_picked updates status and calculates wait_time."""
        self.request.mark_picked(t=10)
        self.assertEqual(self.request.status, "PICKED")
        self.assertEqual(self.request.wait_time, 10)

    def test_mark_picked_with_different_creation_time(self):
        """Test mark_picked calculates wait_time correctly from creation_time."""
        request = Request(id=2, pickup=self.pickup, dropoff=self.dropoff, creation_time=5)
        request.mark_picked(t=15)
        self.assertEqual(request.status, "PICKED")
        self.assertEqual(request.wait_time, 10)

    def test_mark_delivered(self):
        """Test that mark_delivered updates status and calculates wait_time."""
        self.request.mark_delivered(t=20)
        self.assertEqual(self.request.status, "DELIVERED")
        self.assertEqual(self.request.wait_time, 20)

    def test_mark_delivered_with_different_creation_time(self):
        """Test mark_delivered calculates wait_time correctly from creation_time."""
        request = Request(id=3, pickup=self.pickup, dropoff=self.dropoff, creation_time=5)
        request.mark_delivered(t=25)
        self.assertEqual(request.status, "DELIVERED")
        self.assertEqual(request.wait_time, 20)

    def test_mark_expired(self):
        """Test that mark_expired updates status and calculates wait_time."""
        self.request.mark_expired(t=30)
        self.assertEqual(self.request.status, "EXPIRED")
        self.assertEqual(self.request.wait_time, 30)

    def test_mark_expired_with_different_creation_time(self):
        """Test mark_expired calculates wait_time correctly from creation_time."""
        request = Request(id=4, pickup=self.pickup, dropoff=self.dropoff, creation_time=5)
        request.mark_expired(t=35)
        self.assertEqual(request.status, "EXPIRED")
        self.assertEqual(request.wait_time, 30)

    def test_update_wait(self):
        """Test that update_wait calculates correct wait_time."""
        self.request.update_wait(current_time=15)
        self.assertEqual(self.request.wait_time, 15)

    def test_update_wait_with_different_creation_time(self):
        """Test update_wait with non-zero creation_time."""
        request = Request(id=5, pickup=self.pickup, dropoff=self.dropoff, creation_time=10)
        request.update_wait(current_time=25)
        self.assertEqual(request.wait_time, 15)

    def test_request_status_transitions(self):
        """Test a sequence of status transitions through request lifecycle."""
        # Initial state
        self.assertEqual(self.request.status, "WAITING")

        # Assign to driver
        self.request.mark_assigned(driver_id=1)
        self.assertEqual(self.request.status, "ASSIGNED")
        self.assertEqual(self.request.assigned_driver_id, 1)

        # Pick up the request
        self.request.mark_picked(t=10)
        self.assertEqual(self.request.status, "PICKED")
        self.assertEqual(self.request.wait_time, 10)

        # Deliver the request
        self.request.mark_delivered(t=20)
        self.assertEqual(self.request.status, "DELIVERED")
        self.assertEqual(self.request.wait_time, 20)


if __name__ == '__main__':
    unittest.main()