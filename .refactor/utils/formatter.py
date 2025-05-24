"""
Formatter utilities for the refactored implementation.
This module provides text formatting functions used throughout the application.
"""


class TextFormatter:
    """A utility class for formatting text in a consistent way."""

    @staticmethod
    def format_phone_number(phone_number: str) -> str:
        """
        Format a phone number with dashes in the appropriate positions.

        Args:
            phone_number: The phone number to format.

        Returns:
            str: The formatted phone number.
        """
        if '-' in phone_number:
            return phone_number  # Skip formatting if '-' already present

        if len(phone_number) == 10:
            return f"{phone_number[:4]}-{phone_number[4:7]}-{phone_number[7:]}"
        elif len(phone_number) == 7:
            return f"{phone_number[:3]}-{phone_number[3:]}"
        elif len(phone_number) == 9:
            return f"{phone_number[:2]}-{phone_number[2:5]}-{phone_number[5:]}"

        return phone_number  # Return unformatted if no pattern matches

    @staticmethod
    def format_plate_number(part1: str, part2: str) -> str:
        """
        Format a license plate number by combining the two parts with a dash.

        Args:
            part1: The first part of the plate number.
            part2: The second part of the plate number.

        Returns:
            str: The formatted plate number.
        """
        return f"{part1.upper()}-{part2.upper()}"

    @staticmethod
    def parse_plate_number(plate: str) -> tuple:
        """
        Parse a formatted plate number into its component parts.

        Args:
            plate: The formatted plate number (e.g., "ABC-1234").

        Returns:
            tuple: A tuple containing the two parts of the plate number.
                  If the plate doesn't contain a dash, returns (plate, '').
        """
        if '-' in plate:
            return tuple(plate.split('-', 1))
        return (plate, '')
