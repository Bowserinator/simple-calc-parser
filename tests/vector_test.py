import unittest
import os, sys

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(current))

from calc.vector import Vector

# Should be in setUp() but whatever
i = (-1) ** 0.5
a = Vector ([1, 2, 3])
b = Vector([-1, 0.5, i])


class TestVectorMethods(unittest.TestCase):
    def assertArrayAlmostEqual(self, a, b):
        assert len(a) == len(b)
        assert all([abs(a[i] - b[i]) < 1e-7 for i in range(len(a))])

    def test_add(self):
        self.assertArrayAlmostEqual((a + b).items, [0, 2.5, 3 + i])
        self.assertArrayAlmostEqual((b + a).items, [0, 2.5, 3 + i])
        self.assertArrayAlmostEqual((a + 1).items, [2, 3, 4])
        self.assertArrayAlmostEqual((1 + a).items, [2, 3, 4])
        self.assertArrayAlmostEqual((a + i).items, [1 + i, 2 + i, 3 + i])

    def test_sub(self):
        self.assertArrayAlmostEqual((a - b).items, [2, 1.5, 3 - i])
        self.assertArrayAlmostEqual((b - a).items, [-2, -1.5, i - 3])
        self.assertArrayAlmostEqual((a - 1).items, [0, 1, 2])
        self.assertArrayAlmostEqual((1 - a).items, [0, -1, -2])
        self.assertArrayAlmostEqual((a - i).items, [1 - i, 2 - i, 3 - i])

    def test_mul(self):
        self.assertArrayAlmostEqual((a * b).items, [-1, 1, 3 * i])
        self.assertArrayAlmostEqual((b * a).items, [-1, 1, 3 * i])
        self.assertArrayAlmostEqual((a * 2).items, [2, 4, 6])
        self.assertArrayAlmostEqual((2 * a).items, [2, 4, 6])
        self.assertArrayAlmostEqual((b * i).items, [-i, 0.5 * i, -1])

    def test_div(self):
        self.assertArrayAlmostEqual((a / b).items, [-1, 4, 3 * -i])
        self.assertArrayAlmostEqual((b / a).items, [-1, 0.25, i / 3])
        self.assertArrayAlmostEqual((a / 3).items, [1 / 3, 2 / 3, 3 / 3])
        self.assertArrayAlmostEqual((3 / a).items, [3, 1.5, 1])

    def test_pow(self):
        self.assertArrayAlmostEqual((a ** b).items, [1, 2 ** 0.5, 3 ** i])
        self.assertArrayAlmostEqual((b ** a).items, [-1, 0.25, i ** 3])
        self.assertArrayAlmostEqual((a ** 3).items, [1, 8, 27])
        self.assertArrayAlmostEqual((3 ** a).items, [3, 9, 27])

    def test_floordiv(self):
        c = Vector([6, 11, 16])
        self.assertArrayAlmostEqual((c // a).items, [6, 5, 5])
        self.assertArrayAlmostEqual((a // c).items, [0, 0, 0])
        self.assertArrayAlmostEqual((a // 3).items, [0, 0, 1])
        self.assertArrayAlmostEqual((3 // a).items, [3, 1, 1])

    def test_str(self):
        self.assertEqual(str(a), "[1, 2, 3]")

    def test_len(self):
        self.assertEqual(len(a), 3)

    def test_getitem(self):
        """Test the [] operator works correctly (positive and negative indices)"""
        self.assertEqual(a[0], 1)
        self.assertEqual(a[1], 2)
        self.assertEqual(a[2], 3)
        self.assertEqual(a[-1], 3)

    def test_incompatible_lengths(self):
        """Vectors of 0 length and operations with incompatible lengths should throw"""
        c = Vector([0])
        with self.assertRaises(RuntimeError, msg="Incorrectly added vectors of incompatible sizes"):
            c + a
        with self.assertRaises(RuntimeError, msg="Didn't throw on empty input"):
            c = Vector([])

    def test_non_numeric_items(self):
        """Vectors should not accept non-numeric types"""
        with self.assertRaises(RuntimeError, msg="Didn't throw on string input"):
            c = Vector([1, 2, "3"])
        with self.assertRaises(RuntimeError, msg="Didn't throw on array item"):
            c = Vector([1, 2, [3]])

    def test_not_mutate(self):
        """Vector operations should not mutate the vector"""
        a = Vector([1, 2, 3])
        b = Vector([1, 2, 3])
        c = a + b
        self.assertEqual(a.items, [1, 2, 3])
        self.assertEqual(b.items, [1, 2, 3])
        self.assertEqual(c.items, [2, 4, 6])

    def test_abs(self):
        self.assertAlmostEqual(abs(a), (1 + 2 ** 2 + 3 ** 2) ** 0.5)
        self.assertAlmostEqual(abs(Vector([-1, -2, -3])), (1 + 2 ** 2 + 3 ** 2) ** 0.5)
    
    def test_dot(self):
        self.assertEqual(Vector([1, 2]).dot(Vector([3, 4])), 3 + 8)

if __name__ == '__main__':
    unittest.main()
