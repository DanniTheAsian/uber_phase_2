# tests/mock_objects.py

class MockPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx*dx + dy*dy) ** 0.5


class MockDriver:
    def __init__(self, id=1, x=0, y=0, speed=1.0):
        self.id = id
        self.position = MockPoint(x, y)
        self.speed = speed


class MockRequest:
    def __init__(self, id=1, pickup=None, dropoff=None, wait_time=0):
        self.id = id
        self.pickup = pickup or MockPoint(0, 0)
        self.dropoff = dropoff or MockPoint(1, 1)
        self.wait_time = wait_time


class MockOffer:
    def __init__(self, driver, request, travel_time, reward):
        self.driver = driver
        self.request = request
        self.estimated_travel_time = travel_time
        self.estimated_reward = reward
