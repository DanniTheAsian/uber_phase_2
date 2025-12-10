"""
2D point helpers with basic vector arithmetic.
"""
from math import sqrt

class Point:
    """
    Immutable point in 2D space with common vector operations.

    Attributes:
        x (float): Horizontal coordinate.
        y (float): Vertical coordinate.
    """
    def __init__(self, x:float, y:float) -> None:
        """
        Create a point with explicit coordinates.

        Args:
            x (float): Horizontal coordinate.
            y (float): Vertical coordinate.

        Example:
            >>> p = Point(2, 3)
            >>> (p.x, p.y)
            (2, 3)
        """
        self.x = x
        self.y = y
    
    def distance_to(self, other: "Point") -> float:
        """
        Calculate the Euclidean distance to another point.

        Args:
            other (Point): The point to measure against.

        Returns:
            float: Non-negative Euclidean distance between the points.

        Example:
            >>> Point(0, 0).distance_to(Point(3, 4))
            5.0
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx**2 + dy**2)
    
    def __add__(self, other: "Point") -> "Point":
        """
        Return a new point representing component-wise addition.

        Args:
            other (Point): Point whose coordinates are added.

        Returns:
            Point: Fresh point containing the summed coordinates.

        Example:
            >>> p = Point(1, 2) + Point(3, 4)
            >>> (p.x, p.y)
            (4, 6)
        """
        return Point(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other: "Point") -> "Point":
        """
        Add another point to this one in place.

        Args:
            other (Point): Point whose coordinates are added.

        Returns:
            Point: This point after mutation.

        Example:
            >>> p = Point(1, 1)
            >>> p += Point(2, 3)
            >>> (p.x, p.y)
            (3, 4)
        """
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: "Point") -> "Point":
        """
        Return a new point containing the coordinate differences.

        Args:
            other (Point): Point to subtract.

        Returns:
            Point: Fresh point containing the difference.

        Example:
            >>> p = Point(5, 5) - Point(2, 3)
            >>> (p.x, p.y)
            (3, 2)
        """
        return Point(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other: "Point") -> "Point":
        """
        Subtract another point from this one in place.

        Args:
            other (Point): Point to subtract.

        Returns:
            Point: This point after mutation.

        Example:
            >>> p = Point(5, 5)
            >>> p -= Point(2, 3)
            >>> (p.x, p.y)
            (3, 2)
        """
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __mul__(self, scalar: int | float) -> "Point":
        """
        Scale the point by a scalar and return a new point.

        Args:
            scalar (int | float): Factor to multiply the coordinates by.

        Returns:
            Point: Scaled point with multiplied coordinates.

        Example:
            >>> p = Point(2, 3) * 2
            >>> (p.x, p.y)
            (4, 6)
        """
        return Point(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: int | float) -> "Point":
        """
        Support scalar multiplication with the scalar on the left-hand side.

        Args:
            scalar (int | float): Factor to multiply the coordinates by.

        Returns:
            Point: Scaled point with multiplied coordinates.

        Example:
            >>> p = 2 * Point(2, 3)
            >>> (p.x, p.y)
            (4, 6)
        """
        return self.__mul__(scalar)