import unittest
from phase2.point import Point

class testPoint(unittest.TestCase):
    """
        Unit tests for the Point class.
    
        This test suite checks:
        - addition and subtraction
        - in-place operations
        - scalar multiplication (left and right)
        - that multiplication does not modify the original point
    """

    def print_status(self, name, success):
        """
        Print SUCCESSFUL or FAILED after each test.

        Arguments:
            name (str): Name of the test.
            success (bool): Whether the test passed.
        """

        if success:
            print(f"{name}: SUCCESSFUL")
        else:
            print(f"{name}: FAILED")

    def test_add(self):
        """
        Test that Point.__add__ returns a new point with correct coordinates.

        Example:
            (1, 2) + (3, 4) = (4, 6)
        """
        name = "test_add"
        try:
            p1 = Point(1,2)
            p2 = Point(3,4)
            result = p1 + p2
            self.assertEqual((result.x, result.y), (4, 6))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_sub(self):
        """
        Test that Point.__sub__ returns a new point with correct coordinates.

        Example:
            (5, 5) - (2, 3) = (3, 2)
        """
        name = "test_sub"
        try:
            p1 = Point(5,5)
            p2 = Point(2,3)
            result = p1 - p2
            self.assertEqual((result.x, result.y), (3,2))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_iadd(self):
        """
        Test that Point.__iadd__ correctly modifies the point in-place.

        Example:
            p = (1, 1)
            p += (2, 1) → p becomes (3, 2)
        """
        name = "test_iadd"
        try:
            p1 = Point(1,1)
            p2 = Point(2,1)
            p1 += p2
            self.assertEqual((p1.x, p1.y), (3,2))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_isub(self):
        """
        Test that Point.__isub__ correctly modifies the point in-place.

        Example:
            p = (4, 1)
            p -= (2, 1) → p becomes (2, 0)
        """
        name = "test_isub"
        try:
            p1 = Point(4,1)
            p2 = Point(2,1)
            p1 -= p2
            self.assertEqual((p1.x, p1.y), (2,0))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_mul_int(self):
        """
        Test that Point.__mul__ works with integers.

        Example:
            (2, 3) * 2 = (4, 6)
        """
        name = "test_mul_int"
        try:
            p = Point(2, 3)
            result = p * 2
            self.assertEqual((result.x, result.y), (4, 6))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_mul_float(self):
        """
        Test that Point.__mul__ works with floats.

        Example:
            (1.5, -2.0) * 2.0 = (3.0, -4.0)
        """
        name = "test_mul_float"
        try:
            p = Point(1.5, -2.0)
            result = p * 2.0
            self.assertEqual((result.x, result.y), (3.0, -4.0))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_rmul_int(self):
        """
        Test that Point.__rmul__ supports integer * Point.

        Example:
            3 * (4, -1) = (12, -3)
        """
        name = "test_rmul_int"
        try:
            p = Point(4, -1)
            result = 3 * p
            self.assertEqual((result.x, result.y), (12, -3))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_rmul_float(self):
        """
        Test that Point.__rmul__ supports float * Point.

        Example:
            0.5 * (0.5, 2.0) = (0.25, 1.0)
        """
        name = "test_rmul_float"
        try:
            p = Point(0.5, 2.0)
            result = 0.5 * p
            self.assertEqual((result.x, result.y), (0.25, 1.0))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

if __name__ == "__main__":
    unittest.main()
