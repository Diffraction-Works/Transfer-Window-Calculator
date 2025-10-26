import math

def phase_angle(planet1, planet2, t):
    """
    Calculate the phase angle between two planets at time t.

    :param planet1: Planet object for the first planet
    :param planet2: Planet object for the second planet
    :param t: Time in seconds
    :return: Phase angle in degrees
    """
    lambda1 = math.degrees(planet1.mean_longitude_at_time(t))
    lambda2 = math.degrees(planet2.mean_longitude_at_time(t))
    phi = (lambda2 - lambda1) % 360
    return phi

def transfer_window_time(planet1, planet2, target_phase=0):
    """
    Calculate the time until the next transfer window (phase angle = target_phase).

    :param planet1: Planet object for the departure planet
    :param planet2: Planet object for the arrival planet
    :param target_phase: Target phase angle in degrees (0 for inner to outer, 180 for outer to inner)
    :return: Time in seconds until the next transfer window
    """
    # For simplicity, assume planet1 is inner, planet2 is outer
    # The phase angle changes at rate (n2 - n1)
    n1 = 2 * math.pi / planet1.orbital_period()
    n2 = 2 * math.pi / planet2.orbital_period()
    delta_n = n2 - n1

    if abs(delta_n) < 1e-10:  # Handle near-zero difference to avoid division by very small number
        raise ValueError("Planets have nearly identical orbital periods; transfer window calculation not applicable.")

    # Current phase angle
    phi_current = phase_angle(planet1, planet2, 0)

    # Time to reach target phase
    delta_phi = (target_phase - phi_current) % 360
    t = delta_phi / math.degrees(delta_n)

    return t

def hohmann_transfer_time(planet1, planet2):
    """
    Calculate the Hohmann transfer time between two planets.

    :param planet1: Planet object for the departure planet
    :param planet2: Planet object for the arrival planet
    :return: Transfer time in seconds
    """
    a_transfer = (planet1.a + planet2.a) / 2
    G = 6.67430e-11
    M = planet1.M  # Assuming same central mass
    return math.pi * math.sqrt(a_transfer**3 / (G * M))
