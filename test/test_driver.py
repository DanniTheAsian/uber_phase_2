import unittest
from unittest.mock import Mock, MagicMock, patch
from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request


class TestDriverInitialization(unittest.TestCase):
    """Test Driver initialization and basic attributes."""
    
    def test_driver_creation(self):
        """Test basic Driver creation with required parameters."""
        # Create a mock behaviour
        mock_behaviour = Mock()
        
        driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=2.5,
            behaviour=mock_behaviour
        )
        
        self.assertEqual(driver.id, 1)
        self.assertEqual(driver.position.x, 0)
        self.assertEqual(driver.position.y, 0)
        self.assertEqual(driver.speed, 2.5)
        self.assertEqual(driver.status, "IDLE")
        self.assertIsNone(driver.current_request)
        self.assertEqual(driver.history, [])
        self.assertIsNone(driver.position_at_assignment)
    
    def test_driver_with_optional_parameters(self):
        """Test Driver creation with optional parameters."""
        mock_behaviour = Mock()
        test_request = Request(id = 101, pickup = Point(0,0), dropoff = Point(10,0), creation_time = 0)
        
        driver = Driver(
            id=2,
            position=Point(5, 5),
            speed=3.0,
            behaviour=mock_behaviour,
            status="TO_PICKUP",
            current_request=test_request,
            history=[{"test": "data"}]
        )
        
        self.assertEqual(driver.status, "TO_PICKUP")
        self.assertIsNotNone(driver.current_request)
        assert driver.current_request is not None
        self.assertEqual(driver.current_request.id, 101)
        self.assertEqual(driver.history, [{"test": "data"}])


class TestDriverMovement(unittest.TestCase):
    """Test Driver movement and step functionality."""
    
    def setUp(self):
        """Set up test fixture before each test."""
        self.mock_behaviour = Mock()
        self.driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=2.0,
            behaviour=self.mock_behaviour
        )
    
    def test_step_with_no_target(self):
        """Test step() when driver has no target (should do nothing)."""
       
        initial_position = self.driver.position
        
        self.driver.step(dt=1.0)
        
        
        self.assertEqual(self.driver.position.x, initial_position.x)
        self.assertEqual(self.driver.position.y, initial_position.y)
    
    def test_step_towards_target(self):
        """Test step() moves driver towards target."""
        
        request = Request(
            id = 101,
            pickup = Point(10, 0),
            dropoff = Point(20, 0),
            creation_time = 0
        )

        with patch.object(request, 'mark_assigned'):
            self.driver.assign_request(request, reward = 15.0)
        
        self.driver.step(dt = 1.0)
        self.assertEqual(self.driver.position, Point(2.0, 0.0))
        self.assertEqual(self.driver.status, "TO_PICKUP")


class TestDriverStateTransitions(unittest.TestCase):
    """Test Driver state transitions (pickup/dropoff)."""
    
    def setUp(self):
        self.mock_behaviour = Mock()
        self.driver = Driver(
            id = 1,
            position = Point(0, 0),
            speed = 1.0,
            behaviour = self.mock_behaviour
        )
    
    def test_assign_request(self):
        """Test assigning a request to driver."""

        mock_request = Mock(spec=Request)
        mock_request.id = 101
        mock_request.mark_assigned = Mock()
        
        self.driver.assign_request(mock_request, reward = 50.0)
        

        self.assertEqual(self.driver.current_request, mock_request)
        self.assertEqual(self.driver.status, "TO_PICKUP")
        self.assertEqual(self.driver.position_at_assignment, Point(0, 0))
        mock_request.mark_assigned.assert_called_once_with(1)
    
    def test_complete_pickup(self):
        """Test completing a pickup."""

        mock_request = Mock(spec=Request)
        mock_request.mark_picked = Mock()
        

        self.driver.current_request = mock_request
        self.driver.status = "TO_PICKUP"
        
        self.driver.complete_pickup(time=10)
        

        self.assertEqual(self.driver.status, "TO_DROPOFF")
        mock_request.mark_picked.assert_called_once_with(10)
    
    def test_complete_pickup_wrong_state(self):
        """Test complete_pickup when driver is not in TO_PICKUP state."""
        mock_request = Mock(spec=Request)
        mock_request.mark_picked = Mock()
        

        self.driver.current_request = mock_request
        self.driver.status = "IDLE"
        
        self.driver.complete_pickup(time=10)
        
  
        mock_request.mark_picked.assert_not_called()
        self.assertEqual(self.driver.status, "IDLE")
    
    def test_complete_dropoff(self):
        """Test completing a dropoff."""

        request = Request(
            id=101,
            pickup = Point(0, 0),
            dropoff = Point(10, 0),
            creation_time = 0
        )

        self.driver.current_request = request
        self.driver.status = "TO_DROPOFF"
        self.driver.position_at_assignment = Point(0, 0)
        self.driver.assigned_reward = 50.0

        initial_history_len = len(self.driver.history)

        self.driver.complete_dropoff(time=20)
    
        self.assertEqual(request.status, "DELIVERED")
        
        self.assertIsNone(self.driver.current_request)
        self.assertEqual(self.driver.status, "IDLE")
        self.assertIsNone(self.driver.position_at_assignment)
        self.assertEqual(self.driver.assigned_reward, 0.0)
        
        self.assertEqual(len(self.driver.history), initial_history_len + 1)
        
        history_entry = self.driver.history[-1]
        self.assertEqual(history_entry["driver_id"], 1)
        self.assertEqual(history_entry["request_id"], 101)
        self.assertEqual(history_entry["completion_time"], 20)
        self.assertEqual(history_entry["earnings"], 50.0)
        self.assertEqual(history_entry["total_distance"], 10.0)


class TestDriverTarget(unittest.TestCase):
    """Test Driver.target_point() method."""
    
    def setUp(self):
        self.mock_behaviour = Mock()
        self.driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=1.0,
            behaviour=self.mock_behaviour
        )
    
    def test_target_point_idle(self):
        """Test target_point() returns None when driver is idle."""
 
        self.driver.status = "IDLE"
        self.driver.current_request = None

        result = self.driver.target_point()
        
        self.assertIsNone(result)
    
    def test_target_point_to_pickup(self):
        """Test target_point() returns pickup when status is TO_PICKUP."""
  
        request = Request(
            id=101,
            pickup=Point(5, 5),
            dropoff=Point(10, 10),
            creation_time=0
        )
        self.driver.status = "TO_PICKUP"
        self.driver.current_request = request
        
        result = self.driver.target_point()
        self.assertEqual(result, Point(5, 5))
    
    def test_target_point_to_dropoff(self):
        """Test target_point() returns dropoff when status is TO_DROPOFF."""

        request = Request(
            id=102,
            pickup=Point(0, 0),
            dropoff=Point(8, 6),
            creation_time=0
        )
        self.driver.status = "TO_DROPOFF"
        self.driver.current_request = request
        
        result = self.driver.target_point()
        self.assertEqual(result, Point(8, 6))


if __name__ == '__main__':
    unittest.main(verbosity=2)
