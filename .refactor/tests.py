"""
Comprehensive test script to verify the refactored implementation.
"""

import os
import sys
import unittest
import tempfile
import sqlite3
import json
from unittest.mock import patch, MagicMock

# Ensure proper path for imports
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
refactored_dir = os.path.join(root_dir, '.refactor')

sys.path.insert(0, root_dir)
sys.path.insert(0, refactored_dir)

# Import refactored components
from app.application import Application
from db.database_manager import DatabaseManager
from utils.formatter import TextFormatter
from utils.config_manager import ConfigManager


class TextFormatterTests(unittest.TestCase):
    """Test cases for the TextFormatter utility."""

    def test_phone_number_formatting(self):
        """Test phone number formatting with various formats."""
        # Test standard phone number formats
        self.assertEqual(TextFormatter.format_phone_number("1234567"), "123-4567")
        self.assertEqual(TextFormatter.format_phone_number("0912345678"), "0912-345-678")
        self.assertEqual(TextFormatter.format_phone_number("123456789"), "12-345-6789")

        # Test already formatted numbers
        self.assertEqual(TextFormatter.format_phone_number("123-4567"), "123-4567")

        # Test edge cases
        self.assertEqual(TextFormatter.format_phone_number(""), "")
        self.assertEqual(TextFormatter.format_phone_number("12345"), "12345")  # Unformatted if no pattern match

    def test_plate_number_formatting(self):
        """Test license plate number formatting."""
        # Test standard formatting
        self.assertEqual(TextFormatter.format_plate_number("ABC", "1234"), "ABC-1234")

        # Test capitalization
        self.assertEqual(TextFormatter.format_plate_number("abc", "1234"), "ABC-1234")

        # Test edge cases
        self.assertEqual(TextFormatter.format_plate_number("", ""), "-")

    def test_plate_number_parsing(self):
        """Test license plate number parsing."""
        # Test standard parsing
        part1, part2 = TextFormatter.parse_plate_number("ABC-1234")
        self.assertEqual(part1, "ABC")
        self.assertEqual(part2, "1234")

        # Test without dash
        part1, part2 = TextFormatter.parse_plate_number("ABC1234")
        self.assertEqual(part1, "ABC1234")
        self.assertEqual(part2, "")

        # Test empty string
        part1, part2 = TextFormatter.parse_plate_number("")
        self.assertEqual(part1, "")
        self.assertEqual(part2, "")


class ConfigManagerTests(unittest.TestCase):
    """Test cases for the ConfigManager utility."""

    def setUp(self):
        """Set up temporary configuration environment."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()

        # Store original config file path
        self.original_config_file = ConfigManager.CONFIG_FILE

        # Set config file path to a temporary file
        ConfigManager.CONFIG_FILE = os.path.join(self.temp_dir.name, "test_config.json")

    def tearDown(self):
        """Clean up after tests."""
        # Restore original config file path
        ConfigManager.CONFIG_FILE = self.original_config_file

        # Clean up temporary directory
        self.temp_dir.cleanup()

    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        # Define test configuration
        test_config = {
            'button_font_size': 25,
            'table_font_size': 30,
            'input_font_size': 35
        }

        # Save test configuration
        result = ConfigManager.save_config(test_config)
        self.assertTrue(result)

        # Verify file was created
        self.assertTrue(os.path.exists(ConfigManager.CONFIG_FILE))

        # Load and verify configuration
        loaded_config = ConfigManager.load_config()
        self.assertEqual(loaded_config['button_font_size'], 25)
        self.assertEqual(loaded_config['table_font_size'], 30)
        self.assertEqual(loaded_config['input_font_size'], 35)

    def test_get_config_value(self):
        """Test retrieving specific configuration values."""
        # Save test configuration
        test_config = {'test_key': 'test_value', 'number_key': 42}
        ConfigManager.save_config(test_config)

        # Test getting existing values
        self.assertEqual(ConfigManager.get_config_value('test_key'), 'test_value')
        self.assertEqual(ConfigManager.get_config_value('number_key'), 42)

        # Test default values for non-existent keys
        self.assertEqual(ConfigManager.get_config_value('nonexistent'), None)
        self.assertEqual(ConfigManager.get_config_value('nonexistent', 'default'), 'default')

    def test_set_config_value(self):
        """Test setting individual configuration values."""
        # Create initial configuration
        initial_config = {'existing_key': 'existing_value'}
        ConfigManager.save_config(initial_config)

        # Set a new value
        ConfigManager.set_config_value('new_key', 'new_value')

        # Update an existing value
        ConfigManager.set_config_value('existing_key', 'updated_value')

        # Load and verify
        config = ConfigManager.load_config()
        self.assertEqual(config['new_key'], 'new_value')
        self.assertEqual(config['existing_key'], 'updated_value')

    @patch('utils.config_manager.open')
    def test_error_handling(self, mock_open):
        """Test error handling during configuration operations."""
        # Make open() raise an exception
        mock_open.side_effect = IOError("Test IO Error")

        # Test load_config error handling
        config = ConfigManager.load_config()
        # Should return default config on error
        self.assertEqual(config['button_font_size'], 20)

        # Test save_config error handling
        result = ConfigManager.save_config({'test': 'value'})
        self.assertFalse(result)  # Should return False on error


class DatabaseManagerTests(unittest.TestCase):
    """Test cases for the DatabaseManager."""

    def setUp(self):
        """Set up test database environment."""
        # Create a temporary file for the test database
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)  # Close the file descriptor

        # Store original database file path
        self.original_db_file = DatabaseManager.DATABASE_FILE

        # Set database file path to the temporary file
        DatabaseManager.DATABASE_FILE = self.temp_db_path

        # Initialize test database
        self._initialize_test_db()

    def tearDown(self):
        """Clean up test database."""
        # Restore original database file path
        DatabaseManager.DATABASE_FILE = self.original_db_file

        # Remove temporary database file
        if os.path.exists(self.temp_db_path):
            os.unlink(self.temp_db_path)

    def _initialize_test_db(self):
        """Initialize the test database with schema."""
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plate_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part1 TEXT NOT NULL,
                part2 TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                note TEXT,
                UNIQUE(part1, part2, phone_number)
            )
        ''')
        conn.commit()
        conn.close()

    @patch('db.database_manager.original_add_plate_info')
    def test_add_plate_info(self, mock_add):
        """Test adding plate information to the database."""
        # Set up mock to return True
        mock_add.return_value = None

        # Test successful add
        result = DatabaseManager.add_plate_info("ABC", "1234", "0912345678", "Test note")
        self.assertTrue(result)
        mock_add.assert_called_once_with("ABC", "1234", "0912345678", "Test note")

        # Test with exception
        mock_add.reset_mock()
        mock_add.side_effect = Exception("Test exception")
        result = DatabaseManager.add_plate_info("ABC", "1234", "0912345678", "Test note")
        self.assertFalse(result)

    @patch('db.database_manager.original_get_all_plate_info')
    def test_get_all_plate_info(self, mock_get_all):
        """Test retrieving all plate information from the database."""
        # Set up mock data
        mock_data = [("ABC-1234", "0912345678", "Test note")]
        mock_get_all.return_value = mock_data

        # Test normal retrieval
        result = DatabaseManager.get_all_plate_info()
        self.assertEqual(result, mock_data)
        mock_get_all.assert_called_once()

        # Test with exception
        mock_get_all.reset_mock()
        mock_get_all.side_effect = Exception("Test exception")
        result = DatabaseManager.get_all_plate_info()
        self.assertEqual(result, [])  # Should return empty list on error

    @patch('db.database_manager.original_update_plate_info')
    def test_update_plate_info(self, mock_update):
        """Test updating plate information in the database."""
        # Set up mock to return True
        mock_update.return_value = None

        # Test successful update
        result = DatabaseManager.update_plate_info("ABC", "1234", "0987654321", "Updated note")
        self.assertTrue(result)
        mock_update.assert_called_once_with("ABC", "1234", "0987654321", "Updated note")

        # Test with exception
        mock_update.reset_mock()
        mock_update.side_effect = Exception("Test exception")
        result = DatabaseManager.update_plate_info("ABC", "1234", "0987654321", "Updated note")
        self.assertFalse(result)


@patch('PyQt5.QtWidgets.QApplication')
class ApplicationTests(unittest.TestCase):
    """Test cases for the main Application class."""

    def test_application_initialization(self, mock_qt_app):
        """Test Application initialization."""
        with patch('app.application.MainWindow') as mock_main_window:
            with patch('app.application.initialize_database') as mock_init_db:
                with patch('os.path.exists', return_value=False):
                    # Test initialization when database doesn't exist
                    app = Application()

                    # Verify Qt application was created
                    mock_qt_app.assert_called_once()

                    # Verify database was initialized
                    mock_init_db.assert_called_once()

                    # Verify main window was created
                    mock_main_window.assert_called_once()


def create_test_suite():
    """Create a test suite with all test cases."""
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTest(unittest.makeSuite(TextFormatterTests))
    suite.addTest(unittest.makeSuite(ConfigManagerTests))
    suite.addTest(unittest.makeSuite(DatabaseManagerTests))

    return suite


if __name__ == '__main__':
    # Create and run test suite
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = create_test_suite()
    runner.run(test_suite)
