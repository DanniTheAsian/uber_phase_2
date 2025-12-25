"""
Unit tests for the Driver class in phase2.driver module.
"""

import unittest
from unittest.mock import Mock, patch

from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request


class TestDriverInitialization(unittest.TestCase):
    """
    Test Driver initialization and basic attributes.
    """

    def test_driver_creation(self):
        mock_behaviour = Mock()

        driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=2.5,
            behaviour=mock_behaviour,
        )

        self.assertEqual(driver.id, 1)
        self.assertEqual(driver.position.x, 0)
        self.assertEqual(driver.position.y, 0)
        self.assertEqual(driver.speed, 2.5)
        self.assertEqual(driver.status, "IDLE")
        self.assertIsNone(driver.current_request)
        self.assertEqual(driver.history, [])
        self.assertIsNone(driver.position_at_assignment)

    def test_driver_with_optional_attributes(self):
        mock_behaviour = Mock()
        test_request = Request(
            id=101,
            pickup=Point(0, 0),
            dropoff=Point(10, 0),
            creation_time=0,
        )

        driver = Driver(
            id=2,
            position=Point(5, 5),
            speed=3.0,
            behaviour=mock_behaviour,
            status="TO_PICKUP",
            current_request=test_request,
            history=[{"test": "data"}],
        )

        self.assertEqual(driver.status, "TO_PICKUP")

        self.assertIsNotNone(driver.current_request)
        self.assertEqual(driver.history, [{"test": "data"}])


class TestDriverMovement(unittest.TestCase):
    """
    Test Driver movement and step functionality.
    """

    def setUp(self):
        self.mock_behaviour = Mock()
        self.driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=2.0,
            behaviour=self.mock_behaviour,
        )

    def test_step_with_no_target(self):
        initial_position = self.driver.position
        self.driver.step(dt=1.0)

        self.assertEqual(self.driver.position.x, initial_position.x)
        self.assertEqual(self.driver.position.y, initial_position.y)

    def test_step_towards_pickup(self):
        request = Request(
            id=101,
            pickup=Point(10, 0),
            dropoff=Point(20, 0),
            creation_time=0,
        )

        with patch.object(request, "mark_assigned"):
            self.driver.assign_request(request, current_time=0)

        self.driver.step(dt=1.0)

        self.assertEqual(self.driver.position.x, 2.0)
        self.assertEqual(self.driver.position.y, 0.0)
        self.assertEqual(self.driver.status, "TO_PICKUP")


class TestDriverStateTransitions(unittest.TestCase):
    """
    Test Driver state transitions (pickup/dropoff).
    """

    def setUp(self):
        self.mock_behaviour = Mock()
        self.driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=1.0,
            behaviour=self.mock_behaviour,
        )

    def test_assign_request(self):
        mock_request = Mock(spec=Request)
        mock_request.id = 101
        mock_request.mark_assigned = Mock()

        self.driver.assign_request(mock_request, current_time=0)

        self.assertEqual(self.driver.current_request, mock_request)
        self.assertEqual(self.driver.status, "TO_PICKUP")
        self.assertIsNotNone(self.driver.position_at_assignment)

        self.assertEqual(self.driver.position.x, 0)
        self.assertEqual(self.driver.position.y, 0)

        mock_request.mark_assigned.assert_called_once_with(1)

    def test_complete_pickup(self):
        mock_request = Mock(spec=Request)
        mock_request.mark_picked = Mock()

        self.driver.current_request = mock_request
        self.driver.status = "TO_PICKUP"

        self.driver.complete_pickup(time=10)

        self.assertEqual(self.driver.status, "TO_DROPOFF")
        mock_request.mark_picked.assert_called_once_with(10)

    def test_complete_pickup_wrong_state(self):
        mock_request = Mock(spec=Request)
        mock_request.mark_picked = Mock()

        self.driver.current_request = mock_request
        self.driver.status = "IDLE"

        self.driver.complete_pickup(time=10)

        mock_request.mark_picked.assert_not_called()
        self.assertEqual(self.driver.status, "IDLE")

    def test_complete_dropoff(self):
        request = Request(
            id=101,
            pickup=Point(0, 0),
            dropoff=Point(10, 0),
            creation_time=0,
        )

        self.driver.current_request = request
        self.driver.status = "TO_DROPOFF"
        self.driver.position_at_assignment = Point(0, 0)
        self.driver.assigned_reward = 50.0

        initial_len = len(self.driver.history)

        self.driver.complete_dropoff(time=20)

        self.assertEqual(request.status, "DELIVERED")
        self.assertEqual(self.driver.status, "IDLE")
        self.assertIsNone(self.driver.current_request)
        self.assertEqual(len(self.driver.history), initial_len + 1)

        entry = self.driver.history[-1]
        self.assertEqual(entry["driver_id"], 1)
        self.assertEqual(entry["request_id"], 101)
        self.assertEqual(entry["completion_time"], 20)
        self.assertEqual(entry["earnings"], 50.0)
        self.assertEqual(entry["total_distance"], 10.0)


class TestDriverTargetPoint(unittest.TestCase):
    """
    Test Driver.target_point property.
    """

    def setUp(self):
        self.mock_behaviour = Mock()
        self.driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=1.0,
            behaviour=self.mock_behaviour,
        )

    def test_target_point_idle(self):
        self.driver.status = "IDLE"
        self.driver.current_request = None

        self.assertIsNone(self.driver.target_point)

    def test_target_point_to_pickup(self):
        request = Request(
            id=101,
            pickup=Point(5, 5),
            dropoff=Point(10, 10),
            creation_time=0,
        )

        self.driver.status = "TO_PICKUP"
        self.driver.current_request = request

        target = self.driver.target_point
        assert target is not None
        self.assertEqual(target.x, 5)
        self.assertEqual(target.y, 5)

    def test_target_point_to_dropoff(self):
        request = Request(
            id=102,
            pickup=Point(0, 0),
            dropoff=Point(8, 6),
            creation_time=0,
        )

        self.driver.status = "TO_DROPOFF"
        self.driver.current_request = request

        target = self.driver.target_point
        assert target is not None
        self.assertIsNotNone(target)
        self.assertEqual(target.x, 8)
        self.assertEqual(target.y, 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
