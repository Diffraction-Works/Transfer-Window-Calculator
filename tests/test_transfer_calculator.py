import unittest
import math
from planet import Planet
from transfer_calculator import phase_angle, transfer_window_time, hohmann_transfer_time

class TestTransferCalculator(unittest.TestCase):
    def setUp(self):
        self.earth = Planet("Earth", 149597870700, 5.972e24, 1.989e30, 0.0)
        self.mars = Planet("Mars", 227939366000, 6.39e23, 1.989e30, 0.0)

    def test_phase_angle(self):
        t = 0
        phi = phase_angle(self.earth, self.mars, t)
        self.assertEqual(phi, 0.0)  # Both at initial mean anomaly 0

    def test_transfer_window_time(self):
        t = transfer_window_time(self.earth, self.mars, 0)
        self.assertGreaterEqual(t, 0)  # Should be non-negative time

    def test_hohmann_transfer_time(self):
        t_hohmann = hohmann_transfer_time(self.earth, self.mars)
        self.assertGreater(t_hohmann, 0)  # Should be positive time

    def test_phase_angle_negative_time(self):
        # Test phase_angle with negative time (though GUI validates non-negative)
        t = -86400  # -1 day
        phi = phase_angle(self.earth, self.mars, t)
        # Should still compute, as math allows negative t
        self.assertIsInstance(phi, float)

    def test_transfer_window_time_outer_to_inner(self):
        # Test when planet1 is outer, planet2 is inner (larger a for planet1)
        outer_planet = Planet("Outer", 300000000000, 1e25, 1.989e30, 0.0)
        inner_planet = Planet("Inner", 100000000000, 1e24, 1.989e30, 0.0)
        t = transfer_window_time(outer_planet, inner_planet, 180)  # Target 180 for outer to inner
        self.assertGreaterEqual(t, 0)

    def test_transfer_window_time_identical_periods_error(self):
        # Test identical semi-major axes (same period)
        planet1 = Planet("Planet1", 149597870700, 5.972e24, 1.989e30, 0.0)
        planet2 = Planet("Planet2", 149597870700, 6.39e23, 1.989e30, 0.0)  # Same a, different mass
        with self.assertRaises(ValueError):
            transfer_window_time(planet1, planet2)

    def test_hohmann_transfer_time_large_a(self):
        # Test with very large semi-major axis
        large_planet1 = Planet("Large1", 1e15, 1e25, 1.989e30, 0.0)
        large_planet2 = Planet("Large2", 2e15, 1e25, 1.989e30, 0.0)
        t_hohmann = hohmann_transfer_time(large_planet1, large_planet2)
        self.assertGreater(t_hohmann, 0)
        # Check no overflow (should be finite)
        self.assertTrue(math.isfinite(t_hohmann))

    def test_hohmann_transfer_time_small_a(self):
        # Test with very small semi-major axis
        small_planet1 = Planet("Small1", 1e3, 1e20, 1.989e30, 0.0)
        small_planet2 = Planet("Small2", 2e3, 1e20, 1.989e30, 0.0)
        t_hohmann = hohmann_transfer_time(small_planet1, small_planet2)
        self.assertGreater(t_hohmann, 0)
        # Check accuracy (should be finite and reasonable)
        self.assertTrue(math.isfinite(t_hohmann))

    def test_phase_angle_large_t(self):
        # Test phase_angle with large time to check wrapping
        t = 1e10  # Large time
        phi = phase_angle(self.earth, self.mars, t)
        self.assertGreaterEqual(phi, 0)
        self.assertLess(phi, 360)

if __name__ == '__main__':
    unittest.main()
