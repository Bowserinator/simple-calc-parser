import unittest
import os, sys

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(current))

from calc.vector import Vector
from calc.parse import calc

i = (-1) ** 0.5

class TestParseMethods(unittest.TestCase):
    def assertArrayAlmostEqual(self, a, b, msg=""):
        assert len(a) == len(b)
        assert all([abs(a[i] - b[i]) < 1e-7 for i in range(len(a))])

    def test_basic_math(self):
        self.assertEqual(calc("1 + 1"), 2)
        self.assertEqual(calc("2^5"), 32)
        self.assertEqual(calc("1/-2"), -0.5)
        self.assertEqual(calc("-1/2"), -0.5)
        self.assertEqual(calc("5 % 2"), 1)
        self.assertEqual(calc("10 // 3"), 3)
        self.assertEqual(calc("-3^2"), -9)
        self.assertEqual(calc("(-3)^2"), 9)

    def test_constants(self):
        self.assertAlmostEqual(calc("pi"), 3.1415926535)
        self.assertAlmostEqual(calc("-pi"), -3.1415926535)
        self.assertAlmostEqual(calc("-pi ** 2"), -3.1415926535 ** 2)

    def test_functions_scalar(self):
        self.assertAlmostEqual(calc("cos(pi)"), -1)
        self.assertAlmostEqual(calc("sqrt(-1)"), i)
        self.assertEqual(calc("sqrt(64)"), 8)
        self.assertAlmostEqual(calc("atan(tan(1))"), 1)
        self.assertAlmostEqual(calc("abs(i)"), 1)
        self.assertAlmostEqual(calc("abs(-5)"), 5)

    def test_functions_vector(self):
        self.assertArrayAlmostEqual(calc("sqrt([1, 4, 16])").items, [1, 2, 4])
        self.assertEqual(calc("sum([1, 4, 16])"), 1 + 4 + 16)
        self.assertEqual(calc("max([1,2,3])"), 3)
        self.assertAlmostEqual(calc("prod([1,2,3i])"), 6 * i)

    def test_fancy_functions_vector(self):
        self.assertEqual(calc("sort(3, 2, 1)").items, [1, 2, 3])
        self.assertEqual(calc("sort([3, 2, 1])").items, [1, 2, 3])
        self.assertEqual(calc("rsort(1, 2, 3)").items, [3, 2, 1])
        self.assertEqual(calc("len(1, 2, 3)"), 3)
        self.assertEqual(calc("len([1, 2, 3])"), 3)
        self.assertAlmostEqual(calc("abs([1, 2])"), 5 ** 0.5)
        self.assertAlmostEqual(calc("angle([0, 1], [1, 0])"), 3.1415926535 / 2)
        self.assertAlmostEqual(calc("angle3([0, 1] + [1, 2], [1, 2], [1, 0] + [1, 2])"), 3.1415926535 / 2)

    def test_vararg_functions_scalar(self):
        self.assertEqual(calc("sum(1, 2, 3)"), 6)
        self.assertEqual(calc("max(1, 2, 3)"), 3)
        self.assertEqual(calc("min(1, max(1, 50), max(-1, -2, -3))"), -1)
        self.assertEqual(calc("max(1, max(50), max(-1, -2, -3))"), 50)

    def test_pedmas(self):
        self.assertEqual(calc("1 + 2 * 3^5"), 487)
        self.assertAlmostEqual(calc("1 * 2 / 3"), 2 / 3)
        self.assertAlmostEqual(calc("1 / 2 * 3"), 3 / 2)
        self.assertEqual(calc("1 - 2 + 3"), 2)
        self.assertEqual(calc("1 + 2 - 3"), 0)
        self.assertEqual(calc("2**5 + 2**5"), 64)

    def test_paren(self):
        self.assertEqual(calc("(1 + 2) * 3"), 9)
        self.assertEqual(calc("(1 * (2 + 3)) * 4"), 20)
        self.assertEqual(calc("(((1 + 2)))"), 3)

    def test_plus_minus_sign(self):
        self.assertEqual(calc("-(1 + 2)"), -3)
        self.assertEqual(calc("-cos(0)"), -1)
        self.assertEqual(calc("+(1 + 2)"), 3)
        self.assertEqual(calc("1 + -(2 + 3)"), -4)

    def test_vector(self):
        self.assertArrayAlmostEqual(calc("[1, 2, 3] + 1").items, [2, 3, 4])
        self.assertArrayAlmostEqual(calc("[1, 2, 3] + [1, 2, 3]").items, [2, 4, 6])
        self.assertArrayAlmostEqual(calc("-[1, 2]").items, [-1, -2])

    def test_numbers(self):
        self.assertAlmostEqual(calc("-1"), -1)
        self.assertAlmostEqual(calc("-1.5e-5"), -1.5e-5)
        self.assertAlmostEqual(calc("+1.5e-5"), 1.5e-5)
        self.assertAlmostEqual(calc("1.5e+5"), 1.5e5)
        self.assertAlmostEqual(calc("1.26123"), 1.26123)
        self.assertAlmostEqual(calc("-0.26123"), -0.26123)
        self.assertAlmostEqual(calc("-1e-5"), -1e-5)

    def test_hex_bin_numbers(self):
        self.assertEqual(calc("0xFF"), 255)
        self.assertEqual(calc("0b11111111"), 255)

    def test_invalid_expr(self):
        with self.assertRaises(RuntimeError, msg="Invalid paren usage"):
            calc("(1+2)(3+4)")
        with self.assertRaises(RuntimeError, msg="Invalid paren usage"):
            calc("(1+2))")
        with self.assertRaises(RuntimeError, msg="Invalid paren usage"):
            calc("(1+2) + ()")
        with self.assertRaises(RuntimeError, msg="Invalid paren usage"):
            calc("(1+2)()")
        with self.assertRaises(RuntimeError, msg="Invalid paren usage"):
            calc(")(")
        with self.assertRaises(RuntimeError, msg="Invalid vector usage"):
            calc("][")
        with self.assertRaises(RuntimeError, msg="Invalid vector usage"):
            calc("[1,2,3][4,5,6]")
        with self.assertRaises(RuntimeError, msg="Invalid vector usage"):
            calc("[(1])")
        with self.assertRaises(RuntimeError, msg="Mismatched paren"):
            calc("(rand(rand())")

    def test_invalid_numbers(self):
        with self.assertRaises(ValueError, msg="Invalid number: too many + signs"):
            calc("+++3")
        with self.assertRaises(RuntimeError, msg="Invalid hex number"):
            calc("0xG")
        with self.assertRaises(RuntimeError, msg="Invalid bin number"):
            calc("0b02")
        with self.assertRaises(RuntimeError, msg="Invalid decimal"):
            calc("0.1.2")
        with self.assertRaises(RuntimeError, msg="Invalid E decimal"):
            calc("1.2e1.5")
        with self.assertRaises(RuntimeError, msg="Invalid E decimal"):
            calc("1.2ee5")

    def test_fancy_math_expr(self):
        self.assertAlmostEqual(calc("e^(i * pi)"), -1)
        self.assertAlmostEqual(calc("e^(-i * pi)"), -1)
        self.assertAlmostEqual(calc("i^3"), -i)
        self.assertAlmostEqual(calc("log(i)"), 1.5707963267948966j)
        self.assertAlmostEqual(calc("sin(-sqrt(-1))"), -1.17520119364 * i)
        self.assertTrue(0 <= calc("(1 * urand() * pi)") <= 3.1416)
        self.assertTrue(0 <= calc("rand(rand())") < 2 ** 32)

    def test_all_functions(self):
        self.assertAlmostEqual(calc("sin(pi)"), 0)
        self.assertAlmostEqual(calc("cos(pi)"), -1)
        self.assertAlmostEqual(calc("tan(pi)"), 0)
        self.assertAlmostEqual(calc("asin(sin(0))"), 0)
        self.assertAlmostEqual(calc("acos(cos(0))"), 0)
        self.assertAlmostEqual(calc("atan(tan(0))"), 0)
        self.assertAlmostEqual(calc("atan2(1, 0)"), 3.1415926535897 / 2)
        self.assertAlmostEqual(calc("degrees(pi)"), 180)
        self.assertAlmostEqual(calc("radians(180)"), 3.1415926535)
        self.assertAlmostEqual(calc("abs(-1)"), 1)
        self.assertAlmostEqual(calc("abs(i)"), 1)
        self.assertAlmostEqual(calc("abs(3,4)"), 5)
        self.assertAlmostEqual(calc("abs([3,4])"), 5)
        self.assertAlmostEqual(calc("ceil(1.1)"), 2)
        self.assertAlmostEqual(calc("ceil(1.9)"), 2)
        self.assertAlmostEqual(calc("ceil(-1.1)"), -1)
        with self.assertRaises(TypeError):
            calc("ceil(i)")
        self.assertAlmostEqual(calc("floor(1.1)"), 1)
        self.assertAlmostEqual(calc("floor(1.9)"), 1)
        self.assertAlmostEqual(calc("floor(-1.1)"), -2)
        with self.assertRaises(TypeError):
            calc("floor(i)")
        self.assertAlmostEqual(calc("gcd(10, 15)"), 5)
        self.assertAlmostEqual(calc("lcm(10, 15)"), 30)
        self.assertAlmostEqual(calc("sqrt(-1)"), i)
        self.assertAlmostEqual(calc("sqrt(64)"), 8)
        self.assertAlmostEqual(calc("cbrt(27)"), 3)
        self.assertAlmostEqual(calc("exp2(5)"), 32)
        self.assertAlmostEqual(calc("log(e)"), 1)
        self.assertAlmostEqual(calc("log2(2)"), 1)
        self.assertAlmostEqual(calc("lg(2)"), 1)
        self.assertAlmostEqual(calc("log10(10)"), 1)
        self.assertAlmostEqual(calc("modpow(2, 10, 3)"), 1)
        self.assertAlmostEqual(calc("max(10, 15)"), 15)
        self.assertAlmostEqual(calc("min(10, 15)"), 10)
        with self.assertRaises(TypeError):
            calc("min(i, 10)")
        with self.assertRaises(TypeError):
            calc("max(i, 10)")
        self.assertAlmostEqual(calc("sum([1, 2, i])"), 3 + i)
        self.assertAlmostEqual(calc("sum(1, 2, i)"), 3 + i)
        self.assertAlmostEqual(calc("prod([1, 2, i])"), 2 * i)
        self.assertAlmostEqual(calc("prod(1, 2, i)"), 2 * i)

        self.assertIn(calc("rand(1, 3)"), [1, 2, 3])
        self.assertIn(calc("rand(3)"), [0, 1, 2, 3])
        self.assertTrue(0 <= calc("rand()") < 2 ** 32, msg="0 arg rand in bounds 0 to 2^32-1")

        self.assertTrue(0 <= calc("urand(0, 10)") <= 10, msg="2 arg urand should be in bounds 0-10")
        self.assertTrue(0 <= calc("urand(3)") <= 3, msg="1 arg urand should be in bounds 0-3")
        self.assertTrue(0 <= calc("urand()") <= 1, msg="0 arg urand should be in bounds 0-1")

        self.assertEqual(calc("dot([1,2],[3,4])"), 3 + 8)
        with self.assertRaises(RuntimeError):
            calc("dot(1,2)")
        with self.assertRaises(RuntimeError):
            calc("dot([1,2],[1])")
        with self.assertRaises(RuntimeError):
            calc("cross([1,2],[1])")
        with self.assertRaises(RuntimeError):
            calc("cross([1,2,3,4],[1,2,3,4])")
        self.assertEqual(calc("cross([1,2,3],[4,5,6])").items, [-3, 6, -3])
        

if __name__ == '__main__':
    unittest.main()
