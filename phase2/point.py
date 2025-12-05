"""Docstring"""
from math import sqrt

class Point:
    """Docstring"""
    def __init__(self, x:float, y:float) -> None:
        """Docstring"""
        self.x = x
        self.y = y
    
    def distance_to(self, other: "Point") -> float:
        """Docstring
        >>> self.x = 0
        >>> self.y = 0
        >>> other.x = 3
        >>> other.y = 4
        >>> point1 = Point(self.x, self.y)
        >>> point2 = Point(other.x, other.y)
        >>> point1.distance_to(point2)
        5.0
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx**2 + dy**2)
    
    def __add__(self, other: "Point") -> "Point":
        """Docstring"""
        return Point(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other: "Point") -> "Point":
        """Docstring"""
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: "Point") -> "Point":
        """Docstring"""
        return Point(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other: "Point") -> "Point":
        """Docstring"""
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __mul__(self, scalar: int | float) -> "Point":
        """Docstring"""
        return Point(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: int | float) -> "Point":
        """docstring"""
        return self.__mul__(scalar)