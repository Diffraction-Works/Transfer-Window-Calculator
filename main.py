"""
Transfer Window Calculator

A GUI application for calculating transfer windows between two planets using orbital mechanics.
"""
import customtkinter as ctk
from tkinter import messagebox
import math
import logging
from typing import Optional
from planet import Planet
from transfer_calculator import phase_angle, transfer_window_time, hohmann_transfer_time

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

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
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("Transfer Window Calculator")
        self.root.geometry("800x600")

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Create menu bar
        self.create_menu_bar()

        # Appearance toggle
        self.appearance_mode_button = ctk.CTkButton(self.root, text="Toggle Dark/Light", command=self.toggle_appearance)
        self.appearance_mode_button.pack(pady=5)

        # Initialize input attributes
        self.planet1_name: Optional[ctk.CTkEntry] = None
        self.planet1_a: Optional[ctk.CTkEntry] = None
        self.planet1_mass: Optional[ctk.CTkEntry] = None
        self.planet1_theta0: Optional[ctk.CTkEntry] = None
        self.planet2_name: Optional[ctk.CTkEntry] = None
        self.planet2_a: Optional[ctk.CTkEntry] = None
        self.planet2_mass: Optional[ctk.CTkEntry] = None
        self.planet2_theta0: Optional[ctk.CTkEntry] = None
        self.central_mass: Optional[ctk.CTkEntry] = None
        self.time_days: Optional[ctk.CTkEntry] = None

        # Input fields
        self.create_input_fields()

        # Output fields
        self.create_output_fields()

        # Calculate button
        self.calculate_button = ctk.CTkButton(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)

    def create_menu_bar(self) -> None:
        """
        Create the help button.
        """
        self.help_button = ctk.CTkButton(self.root, text="Help", command=self.show_help)
        self.help_button.pack(pady=5, padx=5, anchor="ne")

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

    def toggle_appearance(self) -> None:
        """
        Toggle between dark and light mode.
        """
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def create_input_fields(self) -> None:
        """
        Create the input fields for planet parameters.
        """
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")

        title_label = ctk.CTkLabel(input_frame, text="Planet Parameters", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.create_planet1_inputs(input_frame)
        self.create_planet2_inputs(input_frame)
        self.create_central_inputs(input_frame)

    def create_planet1_inputs(self, input_frame: ctk.CTkFrame) -> None:
        """
        Create input fields for Planet 1.
        """
        self._create_planet_inputs(input_frame, 1, "Planet 1", self.planet1_name, self.planet1_a, self.planet1_mass, self.planet1_theta0,
                                   DEFAULT_PLANET1_NAME, str(DEFAULT_PLANET1_A_KM), str(DEFAULT_PLANET1_MASS), str(DEFAULT_PLANET1_THETA0))

    def create_planet2_inputs(self, input_frame: ctk.CTkFrame) -> None:
        """
        Create input fields for Planet 2.
        """
        self._create_planet_inputs(input_frame, 5, "Planet 2", self.planet2_name, self.planet2_a, self.planet2_mass, self.planet2_theta0,
                                   DEFAULT_PLANET2_NAME, str(DEFAULT_PLANET2_A_KM), str(DEFAULT_PLANET2_MASS), str(DEFAULT_PLANET2_THETA0))

    def create_central_inputs(self, input_frame: ctk.CTkFrame) -> None:
        """
        Create input fields for central body mass and time.
        """
        # Central body
        ctk.CTkLabel(input_frame, text="Central Body Mass (kg):").grid(row=8, column=0, sticky="w", padx=5, pady=2)
        self.central_mass = ctk.CTkEntry(input_frame)
        self.central_mass.grid(row=8, column=1, padx=5, pady=2)
        self.central_mass.insert(0, str(DEFAULT_CENTRAL_MASS))

        # Time
        ctk.CTkLabel(input_frame, text="Time (days):").grid(row=9, column=0, sticky="w", padx=5, pady=2)
        self.time_days = ctk.CTkEntry(input_frame)
        self.time_days.grid(row=9, column=1, padx=5, pady=2)
        self.time_days.insert(0, str(DEFAULT_TIME_DAYS))

    def _create_planet_inputs(self, frame: ctk.CTkFrame, start_row: int, label_prefix: str,
                              name_entry: Optional[ctk.CTkEntry], a_entry: Optional[ctk.CTkEntry],
                              mass_entry: Optional[ctk.CTkEntry], theta_entry: Optional[ctk.CTkEntry],
                              default_name: str, default_a: str, default_mass: str, default_theta: str) -> None:
        """
        Helper method to create input fields for a planet.
        """
        attr_prefix = label_prefix.lower().replace(' ', '')

        ctk.CTkLabel(frame, text=f"{label_prefix} Name:").grid(row=start_row, column=0, sticky="w", padx=5, pady=2)
        name_entry = ctk.CTkEntry(frame)
        name_entry.grid(row=start_row, column=1, padx=5, pady=2)
        name_entry.insert(0, default_name)
        setattr(self, f"{attr_prefix}_name", name_entry)

        ctk.CTkLabel(frame, text="Semi-major Axis (km):").grid(row=start_row+1, column=0, sticky="w", padx=5, pady=2)
        a_entry = ctk.CTkEntry(frame)
        a_entry.grid(row=start_row+1, column=1, padx=5, pady=2)
        a_entry.insert(0, default_a)
        setattr(self, f"{attr_prefix}_a", a_entry)

        ctk.CTkLabel(frame, text="Mass (kg):").grid(row=start_row+2, column=0, sticky="w", padx=5, pady=2)
        mass_entry = ctk.CTkEntry(frame)
        mass_entry.grid(row=start_row+2, column=1, padx=5, pady=2)
        mass_entry.insert(0, default_mass)
        setattr(self, f"{attr_prefix}_mass", mass_entry)

        ctk.CTkLabel(frame, text="Initial Mean Anomaly (deg):").grid(row=start_row+3, column=0, sticky="w", padx=5, pady=2)
        theta_entry = ctk.CTkEntry(frame)
        theta_entry.grid(row=start_row+3, column=1, padx=5, pady=2)
        theta_entry.insert(0, default_theta)
        setattr(self, f"{attr_prefix}_theta0", theta_entry)

    def create_output_fields(self):
        output_frame = ctk.CTkFrame(self.root)
        output_frame.pack(pady=10, padx=10, fill="x")

        title_label = ctk.CTkLabel(output_frame, text="Results", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=5)

        self.phase_angle_label = ctk.CTkLabel(output_frame, text="Phase Angle: ")
        self.phase_angle_label.pack(anchor="w", padx=5, pady=2)

        self.transfer_time_label = ctk.CTkLabel(output_frame, text="Time to Transfer Window: ")
        self.transfer_time_label.pack(anchor="w", padx=5, pady=2)

        self.hohmann_time_label = ctk.CTkLabel(output_frame, text="Hohmann Transfer Time: ")
        self.hohmann_time_label.pack(anchor="w", padx=5, pady=2)

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
            self.phase_angle_label.configure(text=f"Phase Angle: {phi:.2f} degrees")
            self.transfer_time_label.configure(text=f"Time to Transfer Window: {transfer_t / DAYS_TO_SECONDS:.2f} days")
            self.hohmann_time_label.configure(text=f"Hohmann Transfer Time: {hohmann_t / DAYS_TO_SECONDS:.2f} days")

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

    def _get_positive_float(self, entry: Optional[ctk.CTkEntry], field_name: str) -> float:
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

    def _get_theta0(self, entry: Optional[ctk.CTkEntry], field_name: str) -> float:
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

    def _get_non_negative_float(self, entry: Optional[ctk.CTkEntry], field_name: str) -> float:
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
    root = ctk.CTk()
    app = TransferWindowCalculator(root)
    root.mainloop()
