"""Docstring"""
from math import sqrt

class Point:
    """Docstring"""
    def __init__(self, x:float, y:float) -> None:
        """Docstring"""
        self.x = x
        self.y = y
    
    def distance_to(self, other: "Point") -> float:
        """Docstring"""
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx**2 + dy**2)
    
    def __add__(self, other: "Point") -> "Point":
        """Docstring"""
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Point") -> "Point":
        """Docstring"""
        return Point(self.x - other.x, self.y - other.y)
    
    def __iadd__(self, other: "Point") -> "Point":
        """Docstring"""
        self.x += other.x
        self.y += other.y
        return self
    
    def __isub__(self, other: "Point") -> "Point":
        """Docstring"""
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __mul__(self, other: "Point") -> "Point":
        """Docstring"""
        return Point(self.x * other.x, self.y * other.y)
    
    def __rmul__(self, other: "Point") -> "Point":
        """Docstring"""
        self.x *= other.x
        self.y *= other.y
        return self.__mul__(other)