import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from converter import convert, find_category, list_units, main


class ConvertTest(unittest.TestCase):

    def test_length(self):
        self.assertAlmostEqual(convert(10, "km", "mi"), 6.213711922, places=6)
        self.assertAlmostEqual(convert(12, "in", "ft"), 1.0)

    def test_weight(self):
        self.assertAlmostEqual(convert(1, "kg", "lb"), 2.204622622, places=6)
        self.assertAlmostEqual(convert(16, "oz", "lb"), 1.0)

    def test_volume(self):
        self.assertAlmostEqual(convert(1, "gal", "l"), 3.785411784)
        self.assertAlmostEqual(convert(2, "cup", "pt"), 1.0)

    def test_temperature(self):
        self.assertAlmostEqual(convert(100, "c", "f"), 212.0)
        self.assertAlmostEqual(convert(-40, "f", "c"), -40.0)
        self.assertAlmostEqual(convert(0, "k", "c"), -273.15)
        self.assertAlmostEqual(convert(32, "f", "k"), 273.15)

    def test_below_absolute_zero_rejected(self):
        for value, unit in ((-273.16, "c"), (-460, "f"), (-1, "k")):
            with self.assertRaises(ValueError):
                convert(value, unit, "c")
        self.assertAlmostEqual(convert(-459.67, "f", "k"), 0.0)

    def test_same_unit(self):
        self.assertEqual(convert(5, "m", "m"), 5)

    def test_case_insensitive(self):
        self.assertAlmostEqual(convert(1, "KM", "M"), 1000.0)
        self.assertAlmostEqual(convert(0, "C", "F"), 32.0)

    def test_incompatible_units(self):
        with self.assertRaises(ValueError):
            convert(1, "kg", "m")

    def test_unknown_unit(self):
        with self.assertRaises(ValueError):
            convert(1, "parsec", "m")


class CategoryTest(unittest.TestCase):

    def test_categories(self):
        self.assertEqual(find_category("mi"), "length")
        self.assertEqual(find_category("lb"), "weight")
        self.assertEqual(find_category("tbsp"), "volume")
        self.assertEqual(find_category("K"), "temperature")

    def test_list_units_mentions_every_category(self):
        listing = list_units()
        for category in ("length", "weight", "volume", "temperature"):
            self.assertIn(category, listing)


class MainTest(unittest.TestCase):

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_prints_conversion(self):
        code, out, _ = self.run_main(["10", "km", "mi"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "10 km = 6.21371 mi")

    def test_negative_value(self):
        code, out, _ = self.run_main(["-40", "c", "f"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "-40 c = -40 f")

    def test_list_option(self):
        code, out, _ = self.run_main(["--list"])
        self.assertEqual(code, 0)
        self.assertIn("length:", out)

    def test_error_returns_nonzero(self):
        code, _, err = self.run_main(["1", "kg", "mi"])
        self.assertEqual(code, 1)
        self.assertIn("Cannot convert", err)


if __name__ == "__main__":
    unittest.main()
