import unittest
from unittest.mock import Mock, patch, MagicMock
from main import TransferWindowCalculator
from planet import Planet

class TestTransferWindowCalculator(unittest.TestCase):
    def setUp(self):
        self.root = MagicMock()
        self.app = TransferWindowCalculator(self.root)

        # Mock entry fields
        self.app.planet1_name = MagicMock()  # type: ignore
        self.app.planet1_a = MagicMock()  # type: ignore
        self.app.planet1_mass = MagicMock()  # type: ignore
        self.app.planet1_theta0 = MagicMock()  # type: ignore
        self.app.planet2_name = MagicMock()  # type: ignore
        self.app.planet2_a = MagicMock()  # type: ignore
        self.app.planet2_mass = MagicMock()  # type: ignore
        self.app.planet2_theta0 = MagicMock()  # type: ignore
        self.app.central_mass = MagicMock()  # type: ignore
        self.app.time_days = MagicMock()  # type: ignore

        # Mock labels
        self.app.phase_angle_label = MagicMock()  # type: ignore
        self.app.transfer_time_label = MagicMock()  # type: ignore
        self.app.hohmann_time_label = MagicMock()  # type: ignore

        # Mock the getattr calls in _get_planet_data
        self.app.planet1_name = MagicMock()  # type: ignore
        self.app.planet1_a = MagicMock()  # type: ignore
        self.app.planet1_mass = MagicMock()  # type: ignore
        self.app.planet1_theta0 = MagicMock()  # type: ignore
        self.app.planet2_name = MagicMock()  # type: ignore
        self.app.planet2_a = MagicMock()  # type: ignore
        self.app.planet2_mass = MagicMock()  # type: ignore
        self.app.planet2_theta0 = MagicMock()  # type: ignore

    @patch('main.messagebox.showerror')
    def test_calculate_valid_inputs(self, mock_showerror):
        # Set return values for entry gets
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        # Check that labels were updated
        self.app.phase_angle_label.config.assert_called_once()  # type: ignore
        self.app.transfer_time_label.config.assert_called_once()  # type: ignore
        self.app.hohmann_time_label.config.assert_called_once()  # type: ignore

        # Ensure no error was shown
        mock_showerror.assert_not_called()

    @patch('main.messagebox.showerror')
    def test_calculate_invalid_inputs(self, mock_showerror):
        # Mock invalid input
        self.app.planet1_a.get.return_value = "invalid"  # type: ignore

        self.app.calculate()

        # Check that error was shown
        mock_showerror.assert_called_with("Input Error", "Semi-major axis for Planet 1 must be a valid positive number.")

    @patch('main.messagebox.showerror')
    def test_calculate_empty_name(self, mock_showerror):
        # Set valid inputs except empty name
        self.app.planet1_name.get.return_value = ""  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Planet 1 name cannot be empty.")

    @patch('main.messagebox.showerror')
    def test_calculate_negative_a(self, mock_showerror):
        self.app.planet1_a.get.return_value = "-100"  # type: ignore
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Semi-major axis for Planet 1 must be a valid positive number.")

    @patch('main.messagebox.showerror')
    def test_calculate_zero_mass(self, mock_showerror):
        self.app.planet1_mass.get.return_value = "0"  # type: ignore
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Mass for Planet 1 must be a valid positive number.")

    @patch('main.messagebox.showerror')
    def test_calculate_invalid_theta0(self, mock_showerror):
        self.app.planet1_theta0.get.return_value = "invalid"  # type: ignore
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Initial Mean Anomaly for Planet 1 must be a valid number between 0 and 360.")

    @patch('main.messagebox.showerror')
    def test_calculate_theta0_negative(self, mock_showerror):
        self.app.planet1_theta0.get.return_value = "-1"  # type: ignore
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Initial Mean Anomaly for Planet 1 must be a valid number between 0 and 360.")

    @patch('main.messagebox.showerror')
    def test_calculate_theta0_over_360(self, mock_showerror):
        self.app.planet1_theta0.get.return_value = "361"  # type: ignore
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Initial Mean Anomaly for Planet 1 must be a valid number between 0 and 360.")

    @patch('main.messagebox.showerror')
    def test_calculate_negative_time_days(self, mock_showerror):
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "-1"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Time (days) must be a valid non-negative number.")

    @patch('main.messagebox.showerror')
    def test_calculate_zero_central_mass(self, mock_showerror):
        self.app.central_mass.get.return_value = "0"  # type: ignore
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        mock_showerror.assert_called_with("Input Error", "Central body mass must be a valid positive number.")

    @patch('main.messagebox.showerror')
    @patch('main.phase_angle')
    @patch('main.transfer_window_time')
    @patch('main.hohmann_transfer_time')
    def test_calculate_with_mocked_calculations(self, mock_hohmann, mock_transfer, mock_phase, mock_showerror):
        # Set valid inputs
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Mars"  # type: ignore
        self.app.planet2_a.get.return_value = "227939366.0"  # type: ignore
        self.app.planet2_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "10"  # type: ignore

        # Mock calculation returns
        mock_phase.return_value = 45.0
        mock_transfer.return_value = 864000  # 10 days in seconds
        mock_hohmann.return_value = 259200  # 3 days in seconds

        self.app.calculate()

        # Check labels updated with mocked values
        self.app.phase_angle_label.config.assert_called_with(text="Phase Angle: 45.00 degrees")  # type: ignore
        self.app.transfer_time_label.config.assert_called_with(text="Time to Transfer Window: 10.00 days")  # type: ignore
        self.app.hohmann_time_label.config.assert_called_with(text="Hohmann Transfer Time: 3.00 days")  # type: ignore

        mock_showerror.assert_not_called()

    @patch('main.messagebox.showerror')
    def test_calculate_identical_planets(self, mock_showerror):
        # Set identical planet parameters
        self.app.planet1_name.get.return_value = "Earth"  # type: ignore
        self.app.planet1_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet1_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Earth"  # type: ignore
        self.app.planet2_a.get.return_value = "149597870.7"  # type: ignore
        self.app.planet2_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        # Check that error was shown for identical planets
        mock_showerror.assert_called_with("Input Error", "Planets have nearly identical orbital periods; transfer window calculation not applicable.")

    @patch('main.messagebox.showerror')
    def test_calculate_planet_order_swap(self, mock_showerror):
        # Test with planet1 having larger a than planet2 (outer to inner)
        self.app.planet1_name.get.return_value = "Mars"  # type: ignore
        self.app.planet1_a.get.return_value = "227939366.0"  # type: ignore  # Larger a
        self.app.planet1_mass.get.return_value = "6.39e23"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Earth"  # type: ignore
        self.app.planet2_a.get.return_value = "149597870.7"  # type: ignore  # Smaller a
        self.app.planet2_mass.get.return_value = "5.972e24"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        # Should still calculate, but transfer time might be negative or incorrect due to assumption
        # In current code, delta_n will be negative, leading to potential issues
        # For now, just check it doesn't crash (though ideally should warn or swap)
        self.app.phase_angle_label.config.assert_called()  # type: ignore
        self.app.transfer_time_label.config.assert_called()  # type: ignore
        self.app.hohmann_time_label.config.assert_called()  # type: ignore

    @patch('main.messagebox.showerror')
    def test_calculate_large_values(self, mock_showerror):
        # Test with very large semi-major axes (but different enough to avoid identical periods)
        self.app.planet1_name.get.return_value = "Large1"  # type: ignore
        self.app.planet1_a.get.return_value = "1e10"  # type: ignore  # 1e10 km = 1e13 m
        self.app.planet1_mass.get.return_value = "1e25"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Large2"  # type: ignore
        self.app.planet2_a.get.return_value = "2e10"  # type: ignore  # Different enough
        self.app.planet2_mass.get.return_value = "1e25"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        # Check calculations complete without overflow
        self.app.phase_angle_label.config.assert_called()  # type: ignore
        self.app.transfer_time_label.config.assert_called()  # type: ignore
        self.app.hohmann_time_label.config.assert_called()  # type: ignore
        mock_showerror.assert_not_called()

    @patch('main.messagebox.showerror')
    def test_calculate_small_values(self, mock_showerror):
        # Test with very small semi-major axes
        self.app.planet1_name.get.return_value = "Small1"  # type: ignore
        self.app.planet1_a.get.return_value = "1e-3"  # type: ignore  # 1e-3 km = 1 m
        self.app.planet1_mass.get.return_value = "1e20"  # type: ignore
        self.app.planet1_theta0.get.return_value = "0"  # type: ignore
        self.app.planet2_name.get.return_value = "Small2"  # type: ignore
        self.app.planet2_a.get.return_value = "2e-3"  # type: ignore
        self.app.planet2_mass.get.return_value = "1e20"  # type: ignore
        self.app.planet2_theta0.get.return_value = "0"  # type: ignore
        self.app.central_mass.get.return_value = "1.989e30"  # type: ignore
        self.app.time_days.get.return_value = "0"  # type: ignore

        self.app.calculate()

        # Check calculations complete
        self.app.phase_angle_label.config.assert_called()  # type: ignore
        self.app.transfer_time_label.config.assert_called()  # type: ignore
        self.app.hohmann_time_label.config.assert_called()  # type: ignore
        mock_showerror.assert_not_called()

if __name__ == '__main__':
    unittest.main()
