import unittest
from phase2.request import Request
from phase2.point import Point

class TestRequest(unittest.TestCase):
    def test_mark_assigned(self, driver_id= 42):
        self.assertEqual(driver_id, 42)