import unittest
from phase2.point import Point

class testPoint(unittest.TestCase):

    def print_status(self, name, success):
        if success:
            print(f"{name}: SUCCESSFUL")
        else:
            print(f"{name}: FAILED")

    def test_add(self):
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
        name = "test_rmul_float"
        try:
            p = Point(0.5, 2.0)
            result = 0.5 * p
            self.assertEqual((result.x, result.y), (0.25, 1.0))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_mul_does_not_modify_original(self):
        name = "test_mul_does_not_modify_original"
        try:
            p = Point(3, 3)
            _ = p * 2
            self.assertEqual((p.x, p.y), (3, 3))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise

    def test_rmul_does_not_modify_original(self):
        name = "test_rmul_does_not_modify_original"
        try:
            p = Point(-2, 5)
            _ = 10 * p
            self.assertEqual((p.x, p.y), (-2, 5))
            self.print_status(name, True)
        except Exception:
            self.print_status(name, False)
            raise


if __name__ == "__main__":
    unittest.main()
