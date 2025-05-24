"""
Configuration manager for the refactored implementation.
This module handles loading, saving, and managing application configuration.
"""

import os
import json
from typing import Dict, Any

# Import original code
from app.logger import logger


class ConfigManager:
    """A class to manage configuration settings for the application."""

    CONFIG_FILE = "config.json"

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """
        Load configuration from the config file.

        Returns:
            dict: The configuration settings.
        """
        default_config = {
            'button_font_size': 20,
            'table_font_size': 25,
            'input_font_size': 30
        }

        try:
            if os.path.exists(ConfigManager.CONFIG_FILE):
                with open(ConfigManager.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Ensure all default keys are present
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                # Create config with default values if it doesn't exist
                ConfigManager.save_config(default_config)
                return default_config
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return default_config

    @staticmethod
    def save_config(config: Dict[str, Any]) -> bool:
        """
        Save configuration to the config file.

        Args:
            config: The configuration settings to save.

        Returns:
            bool: True if saving was successful, False otherwise.
        """
        try:
            with open(ConfigManager.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    @staticmethod
    def get_config_value(key: str, default_value: Any = None) -> Any:
        """
        Get a specific configuration value.

        Args:
            key: The configuration key to get.
            default_value: The default value to return if the key doesn't exist.

        Returns:
            The configuration value or the default value.
        """
        config = ConfigManager.load_config()
        return config.get(key, default_value)

    @staticmethod
    def set_config_value(key: str, value: Any) -> bool:
        """
        Set a specific configuration value and save the configuration.

        Args:
            key: The configuration key to set.
            value: The value to set.

        Returns:
            bool: True if setting was successful, False otherwise.
        """
        config = ConfigManager.load_config()
        config[key] = value
        return ConfigManager.save_config(config)
