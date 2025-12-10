from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request


class TestDriverInitialization(TestCase):
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
        test_request = Request(id=101, pickup=Point(0,0), dropoff=Point(10,0), creation_time=0)
        
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


class TestDriverMovement(TestCase):
    """Test Driver movement and step functionality."""
    
    def setUp(self):
        """Set up test fixture before each test."""
        self.mock_behaviour = Mock()
        self.driver = Driver(
            id=1,
            position=Point(0, 0),
            speed=2.0,  # 2 units per tick
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
            id=101,
            pickup=Point(10, 0),
            dropoff=Point(20, 0),
            creation_time=0
        )
        

        with patch.object(self.driver, 'target_point', return_value=Point(10, 0)):
            
            self.driver.step(dt=1.0) 
            self.assertEqual(self.driver.position.x, 2.0) 
            self.assertEqual(self.driver.position.y, 0.0)

