# Transfer Window Calculator

A Python application with a GUI to calculate the phase angle between two planets for optimal transfer windows in orbital mechanics. This tool generalizes beyond specific games like Kerbal Space Program, allowing custom inputs for semi-major axes, masses, and other orbital parameters.

## Features

- **Planet Class**: Define planets with custom orbital parameters (semi-major axis, mass, central body mass, initial mean anomaly).
- **Phase Angle Calculation**: Compute the current phase angle between two planets at a given time.
- **Transfer Window Finder**: Determine the time until the next optimal transfer window (when phase angle is 0° for inner-to-outer transfers or 180° for outer-to-inner).
- **GUI Interface**: User-friendly Tkinter-based GUI for inputting parameters and viewing results.
- **Generalized Calculations**: Works for any two orbiting bodies around a central mass, not limited to specific solar systems.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Diffraction-Works/Transfer-Window-Calculator.git
   cd Transfer-Window-Calculator
   ```

2. Ensure Python 3.x is installed.

3. Install dependencies (if any, but this project uses only standard libraries: `math` and `tkinter`).

4. Run the application:
   ```
   python main.py
   ```

## Usage

1. Launch the application by running `python main.py`.
2. Enter the parameters for Planet 1 and Planet 2:
   - Name
   - Semi-major axis (in meters)
   - Mass (in kg, though not used in calculations)
   - Central body mass (e.g., star mass in kg)
   - Initial mean anomaly (in degrees, default 0)
3. Enter the current time (in seconds, default 0).
4. Click "Calculate" to compute the phase angle and time to next transfer window.
5. View the results in the output area.

## Calculations

The phase angle φ is calculated as:
φ = (λ2 - λ1) mod 360°

Where λ1 and λ2 are the mean longitudes of the planets.

For transfer windows:
- Inner to outer planet: φ = 0°
- Outer to inner planet: φ = 180°

The time to next transfer window is computed based on the relative orbital periods.

## Dependencies

- Python 3.x
- Standard libraries: `math`, `tkinter`

## Contributing

Feel free to submit issues or pull requests for improvements.

## License

This project is open-source. Please check the repository for license details.
