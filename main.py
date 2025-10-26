"""
Transfer Window Calculator

A GUI application for calculating transfer windows between two planets using orbital mechanics.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import math
import logging
from typing import Optional
from planet import Planet
from transfer_calculator import phase_angle, transfer_window_time, hohmann_transfer_time

# Constants
DEFAULT_PLANET1_NAME = "Earth"
DEFAULT_PLANET1_A_KM = 149597870.7
DEFAULT_PLANET1_MASS = 5.972e24
DEFAULT_PLANET1_THETA0 = 0.0

DEFAULT_PLANET2_NAME = "Mars"
DEFAULT_PLANET2_A_KM = 227939366.0
DEFAULT_PLANET2_MASS = 6.39e23
DEFAULT_PLANET2_THETA0 = 0.0

DEFAULT_CENTRAL_MASS = 1.989e30
DEFAULT_TIME_DAYS = 0.0

KM_TO_M = 1000
DAYS_TO_SECONDS = 24 * 3600
PHASE_ANGLE_MAX = 360

class TransferWindowCalculator:
    """
    A GUI application for calculating transfer windows between two planets.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Transfer Window Calculator")
        self.root.geometry("600x500")

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Create menu bar
        self.create_menu_bar()

        # Initialize input attributes
        self.planet1_name: Optional[ttk.Entry] = None
        self.planet1_a: Optional[ttk.Entry] = None
        self.planet1_mass: Optional[ttk.Entry] = None
        self.planet1_theta0: Optional[ttk.Entry] = None
        self.planet2_name: Optional[ttk.Entry] = None
        self.planet2_a: Optional[ttk.Entry] = None
        self.planet2_mass: Optional[ttk.Entry] = None
        self.planet2_theta0: Optional[ttk.Entry] = None
        self.central_mass: Optional[ttk.Entry] = None
        self.time_days: Optional[ttk.Entry] = None

        # Input fields
        self.create_input_fields()

        # Output fields
        self.create_output_fields()

        # Calculate button
        self.calculate_button = ttk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)

    def create_menu_bar(self) -> None:
        """
        Create the menu bar with Help menu.
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_help)

    def show_help(self) -> None:
        """
        Display the help dialog with usage instructions.
        """
        help_text = (
            "Transfer Window Calculator Instructions:\n\n"
            "This application calculates transfer windows between two planets using orbital mechanics.\n\n"
            "Inputs:\n"
            "- Planet 1 & 2 Name: Name of the planets (e.g., Earth, Mars).\n"
            "- Semi-major Axis (km): Distance from the central body to the planet.\n"
            "- Mass (kg): Mass of the planet.\n"
            "- Initial Mean Anomaly (deg): Starting position of the planet in its orbit (0-360 degrees).\n"
            "- Central Body Mass (kg): Mass of the central body (e.g., Sun).\n"
            "- Time (days): Current time in days for phase angle calculation.\n\n"
            "Outputs:\n"
            "- Phase Angle: Angle between the two planets at the given time.\n"
            "- Time to Transfer Window: Time until the optimal transfer opportunity.\n"
            "- Hohmann Transfer Time: Time for a Hohmann transfer orbit between the planets.\n\n"
            "Click 'Calculate' to perform the calculations. Ensure all inputs are valid positive numbers."
        )
        messagebox.showinfo("Help - Instructions", help_text)

    def create_input_fields(self) -> None:
        """
        Create the input fields for planet parameters.
        """
        input_frame = ttk.LabelFrame(self.root, text="Planet Parameters")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Planet 1 inputs
        self._create_planet_inputs(input_frame, 0, "Planet 1", self.planet1_name, self.planet1_a, self.planet1_mass, self.planet1_theta0,
                                   DEFAULT_PLANET1_NAME, str(DEFAULT_PLANET1_A_KM), str(DEFAULT_PLANET1_MASS), str(DEFAULT_PLANET1_THETA0))

        # Planet 2 inputs
        self._create_planet_inputs(input_frame, 4, "Planet 2", self.planet2_name, self.planet2_a, self.planet2_mass, self.planet2_theta0,
                                   DEFAULT_PLANET2_NAME, str(DEFAULT_PLANET2_A_KM), str(DEFAULT_PLANET2_MASS), str(DEFAULT_PLANET2_THETA0))

        # Central body
        ttk.Label(input_frame, text="Central Body Mass (kg):").grid(row=8, column=0, sticky="w")
        self.central_mass = ttk.Entry(input_frame)
        self.central_mass.grid(row=8, column=1, padx=5, pady=2)
        self.central_mass.insert(0, str(DEFAULT_CENTRAL_MASS))

        # Time
        ttk.Label(input_frame, text="Time (days):").grid(row=9, column=0, sticky="w")
        self.time_days = ttk.Entry(input_frame)
        self.time_days.grid(row=9, column=1, padx=5, pady=2)
        self.time_days.insert(0, str(DEFAULT_TIME_DAYS))

    def _create_planet_inputs(self, frame: ttk.LabelFrame, start_row: int, label_prefix: str,
                              name_entry: Optional[ttk.Entry], a_entry: Optional[ttk.Entry],
                              mass_entry: Optional[ttk.Entry], theta_entry: Optional[ttk.Entry],
                              default_name: str, default_a: str, default_mass: str, default_theta: str) -> None:
        """
        Helper method to create input fields for a planet.
        """
        attr_prefix = label_prefix.lower().replace(' ', '')

        ttk.Label(frame, text=f"{label_prefix} Name:").grid(row=start_row, column=0, sticky="w")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=start_row, column=1, padx=5, pady=2)
        name_entry.insert(0, default_name)
        setattr(self, f"{attr_prefix}_name", name_entry)

        ttk.Label(frame, text="Semi-major Axis (km):").grid(row=start_row+1, column=0, sticky="w")
        a_entry = ttk.Entry(frame)
        a_entry.grid(row=start_row+1, column=1, padx=5, pady=2)
        a_entry.insert(0, default_a)
        setattr(self, f"{attr_prefix}_a", a_entry)

        ttk.Label(frame, text="Mass (kg):").grid(row=start_row+2, column=0, sticky="w")
        mass_entry = ttk.Entry(frame)
        mass_entry.grid(row=start_row+2, column=1, padx=5, pady=2)
        mass_entry.insert(0, default_mass)
        setattr(self, f"{attr_prefix}_mass", mass_entry)

        ttk.Label(frame, text="Initial Mean Anomaly (deg):").grid(row=start_row+3, column=0, sticky="w")
        theta_entry = ttk.Entry(frame)
        theta_entry.grid(row=start_row+3, column=1, padx=5, pady=2)
        theta_entry.insert(0, default_theta)
        setattr(self, f"{attr_prefix}_theta0", theta_entry)

    def create_output_fields(self):
        output_frame = ttk.LabelFrame(self.root, text="Results")
        output_frame.pack(pady=10, padx=10, fill="x")

        self.phase_angle_label = ttk.Label(output_frame, text="Phase Angle: ")
        self.phase_angle_label.pack(anchor="w")

        self.transfer_time_label = ttk.Label(output_frame, text="Time to Transfer Window: ")
        self.transfer_time_label.pack(anchor="w")

        self.hohmann_time_label = ttk.Label(output_frame, text="Hohmann Transfer Time: ")
        self.hohmann_time_label.pack(anchor="w")

    def calculate(self) -> None:
        """
        Perform the transfer window calculations and update the output labels.
        """
        try:
            # Validate and get inputs
            planet1_data = self._get_planet_data(1)
            planet2_data = self._get_planet_data(2)
            central_mass = self._get_positive_float(self.central_mass, "Central body mass")
            if self.time_days is None:
                raise ValueError("Time days entry is not initialized.")
            time_days = self._get_non_negative_float(self.time_days, "Time (days)")
            time_seconds = time_days * DAYS_TO_SECONDS

            # Create planets
            planet1 = Planet(planet1_data[0], planet1_data[1], planet1_data[2], central_mass, planet1_data[3])
            planet2 = Planet(planet2_data[0], planet2_data[1], planet2_data[2], central_mass, planet2_data[3])

            # Perform calculations
            phi = phase_angle(planet1, planet2, time_seconds)
            transfer_t = transfer_window_time(planet1, planet2)
            hohmann_t = hohmann_transfer_time(planet1, planet2)

            # Update outputs
            self.phase_angle_label.config(text=f"Phase Angle: {phi:.2f} degrees")
            self.transfer_time_label.config(text=f"Time to Transfer Window: {transfer_t / DAYS_TO_SECONDS:.2f} days")
            self.hohmann_time_label.config(text=f"Hohmann Transfer Time: {hohmann_t / DAYS_TO_SECONDS:.2f} days")

        except ValueError as e:
            self.logger.error(f"Input error: {str(e)}")
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            self.logger.error(f"Calculation error: {str(e)}")
            messagebox.showerror("Calculation Error", f"An unexpected error occurred: {str(e)}")

    def _get_planet_data(self, planet_num: int) -> tuple[str, float, float, float]:
        """
        Get and validate data for a planet.

        :param planet_num: The planet number (1 or 2)
        :return: Tuple of (name, semi_major_axis_m, mass, initial_anomaly_deg)
        """
        name_entry = getattr(self, f"planet{planet_num}_name")
        a_entry = getattr(self, f"planet{planet_num}_a")
        mass_entry = getattr(self, f"planet{planet_num}_mass")
        theta_entry = getattr(self, f"planet{planet_num}_theta0")

        if name_entry is None or a_entry is None or mass_entry is None or theta_entry is None:
            raise ValueError(f"Planet {planet_num} input fields are not initialized.")

        # Assert for type checker
        assert name_entry is not None
        assert a_entry is not None
        assert mass_entry is not None
        assert theta_entry is not None

        name = name_entry.get().strip()
        if not name:
            raise ValueError(f"Planet {planet_num} name cannot be empty.")

        a_km = self._get_positive_float(a_entry, f"Semi-major axis for Planet {planet_num}")
        a_m = a_km * KM_TO_M
        mass = self._get_positive_float(mass_entry, f"Mass for Planet {planet_num}")
        theta0 = self._get_theta0(theta_entry, f"Initial Mean Anomaly for Planet {planet_num}")

        return name, a_m, mass, theta0

    def _get_positive_float(self, entry: Optional[ttk.Entry], field_name: str) -> float:
        """
        Get a positive float value from an entry field.

        :param entry: The entry widget
        :param field_name: Name of the field for error messages
        :return: The positive float value
        """
        if entry is None:
            raise ValueError(f"{field_name} entry is not initialized.")
        try:
            value = float(entry.get())
            if value <= 0:
                raise ValueError(f"{field_name} must be positive.")
            return value
        except ValueError:
            raise ValueError(f"{field_name} must be a valid positive number.")

    def _get_theta0(self, entry: Optional[ttk.Entry], field_name: str) -> float:
        """
        Get and validate theta0 (0-360 degrees) from an entry field.

        :param entry: The entry widget
        :param field_name: Name of the field for error messages
        :return: The validated theta0 value
        """
        if entry is None:
            raise ValueError(f"{field_name} entry is not initialized.")
        try:
            value = float(entry.get())
            if not (0 <= value <= PHASE_ANGLE_MAX):
                raise ValueError(f"{field_name} must be between 0 and {PHASE_ANGLE_MAX} degrees.")
            return value
        except ValueError:
            raise ValueError(f"{field_name} must be a valid number between 0 and {PHASE_ANGLE_MAX}.")

    def _get_non_negative_float(self, entry: Optional[ttk.Entry], field_name: str) -> float:
        """
        Get a non-negative float value from an entry field.

        :param entry: The entry widget
        :param field_name: Name of the field for error messages
        :return: The non-negative float value
        """
        if entry is None:
            raise ValueError(f"{field_name} entry is not initialized.")
        try:
            value = float(entry.get())
            if value < 0:
                raise ValueError(f"{field_name} must be non-negative.")
            return value
        except ValueError:
            raise ValueError(f"{field_name} must be a valid non-negative number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TransferWindowCalculator(root)
    root.mainloop()
