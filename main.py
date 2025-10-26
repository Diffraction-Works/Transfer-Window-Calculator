import tkinter as tk
from tkinter import ttk, messagebox
import math
from planet import Planet
from transfer_calculator import phase_angle, transfer_window_time, hohmann_transfer_time

class TransferWindowCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Transfer Window Calculator")
        self.root.geometry("600x500")

        # Input fields
        self.create_input_fields()

        # Output fields
        self.create_output_fields()

        # Calculate button
        self.calculate_button = ttk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)

    def create_input_fields(self):
        input_frame = ttk.LabelFrame(self.root, text="Planet Parameters")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Planet 1
        ttk.Label(input_frame, text="Planet 1 Name:").grid(row=0, column=0, sticky="w")
        self.planet1_name = ttk.Entry(input_frame)
        self.planet1_name.grid(row=0, column=1, padx=5, pady=2)
        self.planet1_name.insert(0, "Earth")

        ttk.Label(input_frame, text="Semi-major Axis (km):").grid(row=1, column=0, sticky="w")
        self.planet1_a = ttk.Entry(input_frame)
        self.planet1_a.grid(row=1, column=1, padx=5, pady=2)
        self.planet1_a.insert(0, "149597870.7")

        ttk.Label(input_frame, text="Mass (kg):").grid(row=2, column=0, sticky="w")
        self.planet1_mass = ttk.Entry(input_frame)
        self.planet1_mass.grid(row=2, column=1, padx=5, pady=2)
        self.planet1_mass.insert(0, "5.972e24")

        ttk.Label(input_frame, text="Initial Mean Anomaly (deg):").grid(row=3, column=0, sticky="w")
        self.planet1_theta0 = ttk.Entry(input_frame)
        self.planet1_theta0.grid(row=3, column=1, padx=5, pady=2)
        self.planet1_theta0.insert(0, "0")

        # Planet 2
        ttk.Label(input_frame, text="Planet 2 Name:").grid(row=4, column=0, sticky="w")
        self.planet2_name = ttk.Entry(input_frame)
        self.planet2_name.grid(row=4, column=1, padx=5, pady=2)
        self.planet2_name.insert(0, "Mars")

        ttk.Label(input_frame, text="Semi-major Axis (km):").grid(row=5, column=0, sticky="w")
        self.planet2_a = ttk.Entry(input_frame)
        self.planet2_a.grid(row=5, column=1, padx=5, pady=2)
        self.planet2_a.insert(0, "227939366.0")

        ttk.Label(input_frame, text="Mass (kg):").grid(row=6, column=0, sticky="w")
        self.planet2_mass = ttk.Entry(input_frame)
        self.planet2_mass.grid(row=6, column=1, padx=5, pady=2)
        self.planet2_mass.insert(0, "6.39e23")

        ttk.Label(input_frame, text="Initial Mean Anomaly (deg):").grid(row=7, column=0, sticky="w")
        self.planet2_theta0 = ttk.Entry(input_frame)
        self.planet2_theta0.grid(row=7, column=1, padx=5, pady=2)
        self.planet2_theta0.insert(0, "0")

        # Central body
        ttk.Label(input_frame, text="Central Body Mass (kg):").grid(row=8, column=0, sticky="w")
        self.central_mass = ttk.Entry(input_frame)
        self.central_mass.grid(row=8, column=1, padx=5, pady=2)
        self.central_mass.insert(0, "1.989e30")

        # Time
        ttk.Label(input_frame, text="Time (days):").grid(row=9, column=0, sticky="w")
        self.time_days = ttk.Entry(input_frame)
        self.time_days.grid(row=9, column=1, padx=5, pady=2)
        self.time_days.insert(0, "0")

    def create_output_fields(self):
        output_frame = ttk.LabelFrame(self.root, text="Results")
        output_frame.pack(pady=10, padx=10, fill="x")

        self.phase_angle_label = ttk.Label(output_frame, text="Phase Angle: ")
        self.phase_angle_label.pack(anchor="w")

        self.transfer_time_label = ttk.Label(output_frame, text="Time to Transfer Window: ")
        self.transfer_time_label.pack(anchor="w")

        self.hohmann_time_label = ttk.Label(output_frame, text="Hohmann Transfer Time: ")
        self.hohmann_time_label.pack(anchor="w")

    def calculate(self):
        try:
            # Get inputs
            p1_name = self.planet1_name.get()
            p1_a_km = float(self.planet1_a.get())
            if p1_a_km <= 0:
                raise ValueError("Semi-major axis for Planet 1 must be positive.")
            p1_a = p1_a_km * 1000  # Convert km to m
            p1_mass = float(self.planet1_mass.get())
            if p1_mass <= 0:
                raise ValueError("Mass for Planet 1 must be positive.")
            p1_theta0 = float(self.planet1_theta0.get())

            p2_name = self.planet2_name.get()
            p2_a_km = float(self.planet2_a.get())
            if p2_a_km <= 0:
                raise ValueError("Semi-major axis for Planet 2 must be positive.")
            p2_a = p2_a_km * 1000  # Convert km to m
            p2_mass = float(self.planet2_mass.get())
            if p2_mass <= 0:
                raise ValueError("Mass for Planet 2 must be positive.")
            p2_theta0 = float(self.planet2_theta0.get())

            M = float(self.central_mass.get())
            if M <= 0:
                raise ValueError("Central body mass must be positive.")
            t_days = float(self.time_days.get())
            t = t_days * 24 * 3600  # Convert days to seconds

            # Create planets
            planet1 = Planet(p1_name, p1_a, p1_mass, M, p1_theta0)
            planet2 = Planet(p2_name, p2_a, p2_mass, M, p2_theta0)

            # Calculations
            phi = phase_angle(planet1, planet2, t)
            transfer_t = transfer_window_time(planet1, planet2)
            hohmann_t = hohmann_transfer_time(planet1, planet2)

            # Update outputs
            self.phase_angle_label.config(text=f"Phase Angle: {phi:.2f} degrees")
            self.transfer_time_label.config(text=f"Time to Transfer Window: {transfer_t / (24*3600):.2f} days")
            self.hohmann_time_label.config(text=f"Hohmann Transfer Time: {hohmann_t / (24*3600):.2f} days")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TransferWindowCalculator(root)
    root.mainloop()
