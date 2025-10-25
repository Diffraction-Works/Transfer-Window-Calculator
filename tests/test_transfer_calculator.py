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

if __name__ == '__main__':
    unittest.main()
