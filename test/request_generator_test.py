import unittest
from unittest.mock import patch
from phase2.request import Request
from phase2.request_generator import requestGenerator


class TestRequestGenerator(unittest.TestCase):

    @patch("random.random", return_value=0.1)
    @patch("random.uniform", return_value=5.0)
    def test_generate_single_request(self, _mock_uniform, _mock_random):
        """
        Test that a request is generated when random.random() < rate.
        """
        gen = requestGenerator(rate=0.5, width=100, height=100)
        result = gen.maybe_generate(time=50)

        self.assertEqual(len(result), 1)
        req = result[0]

        self.assertIsInstance(req, Request)
        self.assertEqual(req.id, 1)
        self.assertEqual(req.creation_time, 50)
        self.assertEqual(req.pickup.x, 5.0)
        self.assertEqual(req.dropoff.x, 5.0)
        self.assertEqual(gen.next_id, 2)  # id increment test


    @patch("random.random", return_value=0.9)
    def test_no_request_generated(self, _mock_random):
        """
        Test that no request is generated when random.random() >= rate.
        """
        gen = requestGenerator(rate=0.5, width=100, height=100)
        result = gen.maybe_generate(time=10)

        self.assertEqual(result, [])
        self.assertEqual(gen.next_id, 1)  # unchanged


    @patch("random.random", return_value=0.1)
    @patch("random.uniform", return_value=3.14)
    def test_rush_hour_uses_doubled_rate(self, _mock_uniform, _mock_random):
        """
        During rush hour (200–300), effective_rate = rate * 2.
        """
        gen = requestGenerator(rate=0.3, width=50, height=50)
        result = gen.maybe_generate(time=250)  # inside rush hour window

        self.assertEqual(len(result), 1)
        req = result[0]
        self.assertEqual(req.id, 1)
        self.assertEqual(req.creation_time, 250)


    @patch("random.random", return_value=0.1)
    def test_multiple_calls_increment_id(self, _mock_random):
        """
        Each generated request must receive a unique ID.
        """
        gen = requestGenerator(rate=1.0, width=20, height=20)

        r1 = gen.maybe_generate(time=1)
        r2 = gen.maybe_generate(time=2)
        r3 = gen.maybe_generate(time=3)

        self.assertEqual(r1[0].id, 1)
        self.assertEqual(r2[0].id, 2)
        self.assertEqual(r3[0].id, 3)
        self.assertEqual(gen.next_id, 4)


if __name__ == "__main__":
    unittest.main()
