import unittest
import math
from planet import Planet

class TestPlanet(unittest.TestCase):
    def setUp(self):
        self.earth = Planet("Earth", 149597870700, 5.972e24, 1.989e30, 0.0)
        self.mars = Planet("Mars", 227939366000, 6.39e23, 1.989e30, 0.0)

    def test_init(self):
        self.assertEqual(self.earth.name, "Earth")
        self.assertEqual(self.earth.a, 149597870700)
        self.assertEqual(self.earth.mass, 5.972e24)
        self.assertEqual(self.earth.M, 1.989e30)
        self.assertEqual(self.earth.theta0, 0.0)

    def test_orbital_period(self):
        # Approximate orbital period for Earth in seconds
        expected_period = 365.25 * 24 * 3600  # Roughly 3.15576e7 seconds
        actual_period = self.earth.orbital_period()
        self.assertAlmostEqual(actual_period, expected_period, delta=1e6)

    def test_mean_longitude_at_time(self):
        t = 86400  # 1 day in seconds
        expected_longitude = math.radians(360 / 365.25)  # Approximate daily motion
        actual_longitude = self.earth.mean_longitude_at_time(t)
        self.assertAlmostEqual(actual_longitude, expected_longitude, places=5)

if __name__ == '__main__':
    unittest.main()
