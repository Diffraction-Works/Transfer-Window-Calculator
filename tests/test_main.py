import unittest
from unittest.mock import Mock, patch, MagicMock
from main import TransferWindowCalculator
from planet import Planet

class TestTransferWindowCalculator(unittest.TestCase):
    def setUp(self):
        self.root = MagicMock()
        self.app = TransferWindowCalculator(self.root)

        # Mock entry fields
        self.app.planet1_name = MagicMock()
        self.app.planet1_a = MagicMock()
        self.app.planet1_mass = MagicMock()
        self.app.planet1_theta0 = MagicMock()
        self.app.planet2_name = MagicMock()
        self.app.planet2_a = MagicMock()
        self.app.planet2_mass = MagicMock()
        self.app.planet2_theta0 = MagicMock()
        self.app.central_mass = MagicMock()
        self.app.time_days = MagicMock()

        # Mock labels
        self.app.phase_angle_label = MagicMock()
        self.app.transfer_time_label = MagicMock()
        self.app.hohmann_time_label = MagicMock()

    @patch('main.messagebox.showerror')
    def test_calculate_valid_inputs(self, mock_showerror):
        # Set return values for entry gets
        self.app.planet1_name.get.return_value = "Earth"
        self.app.planet1_a.get.return_value = "149597870.7"
        self.app.planet1_mass.get.return_value = "5.972e24"
        self.app.planet1_theta0.get.return_value = "0"
        self.app.planet2_name.get.return_value = "Mars"
        self.app.planet2_a.get.return_value = "227939366.0"
        self.app.planet2_mass.get.return_value = "6.39e23"
        self.app.planet2_theta0.get.return_value = "0"
        self.app.central_mass.get.return_value = "1.989e30"
        self.app.time_days.get.return_value = "0"

        self.app.calculate()

        # Check that labels were updated
        self.app.phase_angle_label.config.assert_called()
        self.app.transfer_time_label.config.assert_called()
        self.app.hohmann_time_label.config.assert_called()

        # Ensure no error was shown
        mock_showerror.assert_not_called()

    @patch('main.messagebox.showerror')
    def test_calculate_invalid_inputs(self, mock_showerror):
        # Mock invalid input
        self.app.planet1_a.get.return_value = "invalid"

        self.app.calculate()

        # Check that error was shown
        mock_showerror.assert_called_with("Error", "Please enter valid numbers for all fields.")

if __name__ == '__main__':
    unittest.main()
