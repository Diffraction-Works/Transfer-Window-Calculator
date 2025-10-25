import math

class Planet:
    def __init__(self, name, semi_major_axis, mass, central_mass, initial_mean_anomaly=0.0):
        """
        Initialize a Planet object.

        :param name: Name of the planet
        :param semi_major_axis: Semi-major axis in meters
        :param mass: Mass of the planet in kg (not used in calculations here)
        :param central_mass: Mass of the central body (e.g., star) in kg
        :param initial_mean_anomaly: Initial mean anomaly in degrees
        """
        self.name = name
        self.a = semi_major_axis
        self.mass = mass
        self.M = central_mass
        self.theta0 = math.radians(initial_mean_anomaly)  # Convert to radians

    def orbital_period(self):
        """
        Calculate the orbital period using Kepler's third law.

        :return: Orbital period in seconds
        """
        G = 6.67430e-11  # Gravitational constant
        return 2 * math.pi * math.sqrt(self.a**3 / (G * self.M))

    def mean_longitude_at_time(self, t):
        """
        Calculate the mean longitude at time t.

        :param t: Time in seconds
        :return: Mean longitude in radians
        """
        n = 2 * math.pi / self.orbital_period()  # Mean motion
        return self.theta0 + n * t
