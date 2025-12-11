"""
A 2D point class with basic math operations.
"""
from math import sqrt

class Point:
    """
    A point in 2D space.
    
    Attributes:
    x (float): x-value.
    y (float): y-value.
    """
    def __init__(self, x:float, y:float) -> None:
        """
        Initialize a Point
        
        Args:
            x (float): x-coordinate.
            y (float): y-coordinate.

        Returns:
            None

        Example:
            >>> p = Point(2,3)
            >>> p.x, p.y
            (2, 3)
        """
        try:
            self.x = float(x)
        except (TypeError, ValueError) as err:
            print(f"Point init x error: {err}")
            self.x = 0.0

        try:
            self.y = float(y)
        except (TypeError, ValueError) as err:
            print(f"Point init y error: {err}")
            self.y = 0.0
    
    def distance_to(self, other: "Point") -> float:
        """
        Calculate the straight-line distance between two points.

        Args:
            other (Point): The point to measure the distance to.

        Returns:
            float: The non-negative distance.

        Example:
            >>> Point(0, 0).distance_to(Point(3, 4))
            5.0
        """
        try:
            dx = self.x - other.x
            dy = self.y - other.y
            return sqrt(dx**2 + dy**2)
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Point distance error: {err}")
            return 0.0
    
    def __add__(self, other: "Point") -> "Point":
        """
        Add two points together (x + x, y + y) and returns a new point
        
        Args:
            other (Point): The point to add.
        
        Returns:
            Point: A new point with the summed coordinates

        Example:
            >>> p = Point(1, 2) + Point(3, 4)
            >>> (p.x, p.y)
            (4, 6)
        """
        try:
            return Point(self.x + other.x, self.y + other.y)
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Point add error: {err}")
            return Point(self.x, self.y)
    
    def __iadd__(self, other: "Point") -> "Point":
        """
        Add another point to this point (in-place)
        
        Args:
            other (Point): the point to add

        return:
            Point: Modified Point

        Example:
            >>> p = Point(1, 1)
            >>> p += Point(2, 3)
            >>> (p.x, p.y)
            (3, 4)
        """
        try:
            self.x += other.x
            self.y += other.y
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Point iadd error: {err}")
        return self

    def __sub__(self, other: "Point") -> "Point":
        """
        Subtract another point and return a new point.

        Args:
            other (Point): The point to subtract.

        Returns:
            Point: A new point containing the difference.

        Example:
            >>> p = Point(5, 5) - Point(2, 3)
            >>> (p.x, p.y)
            (3, 2)
        """
        try:
            return Point(self.x - other.x, self.y - other.y)
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Point sub error: {err}")
            return Point(self.x, self.y)
    
    def __isub__(self, other: "Point") -> "Point":
        """
        Subtract another point from this one (in-place).

        Args:
            other (Point): The point to subtract.

        Returns:
            Point: The modified point.

        Example:
            >>> p = Point(5, 5)
            >>> p -= Point(2, 3)
            >>> (p.x, p.y)
            (3, 2)
        """
        try:
            self.x -= other.x
            self.y -= other.y
        except (AttributeError, TypeError, ValueError) as err:
            print(f"Point isub error: {err}")
        return self
    
    def __mul__(self, scalar: int | float) -> "Point":
        """
        Multiply this point by a scalar and return a new point.

        Args:
            scalar (int | float): The number to multiply with.

        Returns:
            Point: A new scaled point.

        Example:
            >>> p = Point(2, 3) * 2
            >>> (p.x, p.y)
            (4, 6)
        """
        try:
            factor = float(scalar)
        except (TypeError, ValueError) as err:
            print(f"Point mul error: {err}")
            factor = 1.0
        return Point(self.x * factor, self.y * factor)
    
    def __rmul__(self, scalar: int | float) -> "Point":
        """
        Allow scalar * point multiplication.

        Args:
            scalar (int | float): The number to multiply with.

        Returns:
            Point: A new scaled point.

        Example:
            >>> p = 2 * Point(2, 3)
            >>> (p.x, p.y)
            (4, 6)
        """
        return self.__mul__(scalar)