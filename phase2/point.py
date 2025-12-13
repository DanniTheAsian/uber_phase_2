"""
A 2D point class with basic math operations

Modules:
- Math

"""
from math import sqrt


class Point:
    """
    A point in 2D space
    
    Attributes:
    x (float): x-value
    y (float): y-value
    """
    def __init__(self, x:float, y:float) -> None:
        """
        Initialize a Point.

        Args:
            x (float): x-coordinate.
            y (float): y-coordinate.

        Example:
            >>> p = Point(2, 3)
            >>> p.x, p.y
            (2, 3)
        """
        try:
            self.x = float(x)
            self.y = float(y)
        except (TypeError, ValueError) as err:
            raise TypeError("Point coordinates must be numeric") from err

    def distance_to(self, other: "Point") -> float:
        """
        Calculate the Euclidean distance to another point.

        Args:
            other (Point): The other point to measure distance to.

        Returns:
            float: Euclidean distance.

        Example:
            >>> point1 = Point(0, 0)
            >>> point2 = Point(3, 4)
            >>> point1.distance_to(point2)
            5.0
        """
        try:
            dx = self.x - other.x
            dy = self.y - other.y
        except (AttributeError, TypeError) as err:
            raise TypeError("distance_to expects a Point-like object with .x and .y") from err
        return sqrt(dx ** 2 + dy ** 2)

    def __add__(self, other: "Point") -> "Point":
        """Add two points and return a new Point.

        Example:
            >>> p = Point(1, 2) + Point(3, 4)
            >>> (p.x, p.y)
            (4, 6)
        """
        try:
            return Point(self.x + other.x, self.y + other.y)
        except (AttributeError, TypeError) as err:
            raise TypeError("Can only add Point-like objects with .x and .y") from err

    def __iadd__(self, other: "Point") -> "Point":
        """In-place addition with another Point.

        Example:
            >>> p = Point(1, 1)
            >>> p += Point(2, 3)
            >>> (p.x, p.y)
            (3, 4)
        """
        try:
            self.x += other.x
            self.y += other.y
            return self
        except (AttributeError, TypeError) as err:
            raise TypeError("Can only iadd Point-like objects with .x and .y") from err

    def __sub__(self, other: "Point") -> "Point":
        """Subtract another Point and return a new Point.

        Example:
            >>> p = Point(5, 5) - Point(2, 3)
            >>> (p.x, p.y)
            (3, 2)
        """
        try:
            return Point(self.x - other.x, self.y - other.y)
        except (AttributeError, TypeError) as err:
            raise TypeError("Can only subtract Point-like objects with .x and .y") from err

    def __isub__(self, other: "Point") -> "Point":
        """In-place subtraction with another Point.

        Example:
            >>> p = Point(5, 5)
            >>> p -= Point(2, 3)
            >>> (p.x, p.y)
            (3, 2)
        """
        try:
            self.x -= other.x
            self.y -= other.y
            return self
        except (AttributeError, TypeError) as err:
            raise TypeError("Can only isub Point-like objects with .x and .y") from err

    def __mul__(self, scalar: int | float) -> "Point":
        """Multiply this Point by a scalar and return a new Point.

        Example:
            >>> p = Point(2, 3) * 2
            >>> (p.x, p.y)
            (4, 6)
        """
        try:
            s = float(scalar)
        except (TypeError, ValueError) as err:
            raise TypeError("Can only multiply Point by numeric scalar") from err
        return Point(self.x * s, self.y * s)

    def __rmul__(self, scalar: int | float) -> "Point":
        """Allow scalar * Point multiplication.

        Example:
            >>> p = 2 * Point(2, 3)
            >>> (p.x, p.y)
            (4, 6)
        """
        return self.__mul__(scalar)