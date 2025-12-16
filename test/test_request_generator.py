import unittest
from phase2.request_generator import RequestGenerator
from phase2.request import Request


class TestRequestGenerator(unittest.TestCase):
    """Unit tests for the RequestGenerator class."""

    def setUp(self):
        """Create a RequestGenerator with a fixed rate and map size."""
        self.generator = RequestGenerator(rate=1.0, width=100, height=100)

    def test_maybe_generate_returns_list(self):
        """maybe_generate should always return a list."""
        result = self.generator.maybe_generate(time=0)
        self.assertIsInstance(result, list)

    def test_generate_creates_request(self):
        """A request should be generated when the rate is high."""
        requests = self.generator.maybe_generate(time=5)
        self.assertEqual(len(requests), 1)
        self.assertIsInstance(requests[0], Request)

    def test_request_has_correct_time(self):
        """Generated requests should store the correct creation time."""
        time = 10
        requests = self.generator.maybe_generate(time)
        self.assertEqual(requests[0].creation_time, time)

    def test_request_positions_within_bounds(self):
        """Pickup and dropoff positions must be within map boundaries."""
        requests = self.generator.maybe_generate(time=0)
        req = requests[0]

        self.assertTrue(0 <= req.pickup.x <= 100)
        self.assertTrue(0 <= req.pickup.y <= 100)
        self.assertTrue(0 <= req.dropoff.x <= 100)
        self.assertTrue(0 <= req.dropoff.y <= 100)

    def test_next_id_increments(self):
        """Request IDs should increment for each new request."""
        self.generator.maybe_generate(time=0)
        self.generator.maybe_generate(time=1)
        self.assertEqual(self.generator.next_id, 3)


if __name__ == "__main__":
    unittest.main()
