"""
Database utilities for the refactored implementation.
This module builds on the original database module but adds improved error handling,
connection management, and introduces a DatabaseManager class for better organization.
"""

import sqlite3
import os
from typing import List, Tuple, Optional, Any

# Import original code
from app.logger import logger
from db.database import (
    get_connection as original_get_connection,
    add_plate_info as original_add_plate_info,
    get_all_plate_info as original_get_all_plate_info,
    update_plate_info as original_update_plate_info,
    delete_plate_info as original_delete_plate_info,
    filter_plate_info as original_filter_plate_info,
    plate_exists as original_plate_exists,
    plate_and_phone_exists as original_plate_and_phone_exists,
    plate_and_phone_note_exists as original_plate_and_phone_note_exists
)


class DatabaseManager:
    """
    A class to manage database operations with improved error handling and connection management.
    """

    DATABASE_FILE = "database.db"

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """Get a connection to the SQLite database."""
        try:
            conn = sqlite3.connect(DatabaseManager.DATABASE_FILE)
            return conn
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    @staticmethod
    def execute_query(query: str, params: tuple = None, fetch_all: bool = False) -> Any:
        """Execute a SQL query with parameters."""
        conn = None
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            result = None
            if fetch_all:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount

            return result
        except sqlite3.Error as e:
            logger.error(f"Database error executing query: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def add_plate_info(part1: str, part2: str, phone_number: str, note: str) -> bool:
        """Add a new plate info to the database with improved error handling."""
        try:
            # Use the original function to maintain compatibility
            original_add_plate_info(part1, part2, phone_number, note)
            return True
        except Exception as e:
            logger.error(f"Error adding plate info: {e}")
            return False

    @staticmethod
    def get_all_plate_info() -> list:
        """Get all plate info from the database."""
        try:
            # Use the original function to maintain compatibility
            return original_get_all_plate_info()
        except Exception as e:
            logger.error(f"Error getting all plate info: {e}")
            return []

    @staticmethod
    def update_plate_info(part1: str, part2: str, new_phone_number: str, new_note: str) -> bool:
        """Update the phone number and note for an existing plate info."""
        try:
            # Use the original function to maintain compatibility
            original_update_plate_info(part1, part2, new_phone_number, new_note)
            return True
        except Exception as e:
            logger.error(f"Error updating plate info: {e}")
            return False

    @staticmethod
    def delete_plate_info(part1: str, part2: str) -> bool:
        """Delete a plate info from the database."""
        try:
            # Use the original function to maintain compatibility
            original_delete_plate_info(part1, part2)
            return True
        except Exception as e:
            logger.error(f"Error deleting plate info: {e}")
            return False

    @staticmethod
    def filter_plate_info(part1_filter: str, part2_filter: str, phone_filter: str, search_mode: str) -> list:
        """Filter plate info based on the given filters."""
        try:
            # Use the original function to maintain compatibility
            return original_filter_plate_info(part1_filter, part2_filter, phone_filter, search_mode)
        except Exception as e:
            logger.error(f"Error filtering plate info: {e}")
            return []

    @staticmethod
    def plate_exists(part1: str, part2: str) -> bool:
        """Check if the plate info already exists in the database."""
        try:
            # Use the original function to maintain compatibility
            return original_plate_exists(part1, part2)
        except Exception as e:
            logger.error(f"Error checking plate existence: {e}")
            return False

    @staticmethod
    def plate_and_phone_exists(part1: str, part2: str, phone_number: str) -> bool:
        """Check if both plate number and phone number are duplicated in the database."""
        try:
            # Use the original function to maintain compatibility
            return original_plate_and_phone_exists(part1, part2, phone_number)
        except Exception as e:
            logger.error(f"Error checking plate and phone existence: {e}")
            return False

    @staticmethod
    def plate_and_phone_note_exists(part1: str, part2: str, phone_number: str, note: str) -> bool:
        """Check if both plate number, phone number, and note are duplicated in the database."""
        try:
            # Use the original function to maintain compatibility
            return original_plate_and_phone_note_exists(part1, part2, phone_number, note)
        except Exception as e:
            logger.error(f"Error checking plate, phone, and note existence: {e}")
            return False
