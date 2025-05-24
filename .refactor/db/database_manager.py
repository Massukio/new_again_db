"""
Database utilities for the refactored implementation.
This module provides a complete, standalone implementation of the database functionality
with improved error handling and connection management.
"""

import sqlite3
import os
import shutil
from datetime import datetime
from typing import List, Tuple, Optional, Any

# Import from our refactored modules
from ..utils.logger import logger
from .init import initialize_database


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
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            # Check if the plate exists first
            cursor.execute(
                "SELECT * FROM plate_info WHERE part1 = ? AND part2 = ? AND phone_number = ?",
                (part1, part2, phone_number)
            )

            if cursor.fetchone():
                # Update the existing record
                cursor.execute(
                    "UPDATE plate_info SET note = ? WHERE part1 = ? AND part2 = ? AND phone_number = ?",
                    (note, part1, part2, phone_number)
                )
            else:
                # Insert a new record
                cursor.execute(
                    "INSERT INTO plate_info (part1, part2, phone_number, note) VALUES (?, ?, ?, ?)",
                    (part1, part2, phone_number, note)
                )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding plate info: {e}")
            return False

    @staticmethod
    def get_all_plate_info() -> list:
        """Get all plate info from the database."""
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, part1, part2, phone_number, note FROM plate_info")
            result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Error getting all plate info: {e}")
            return []

    @staticmethod
    def update_plate_info(part1: str, part2: str, new_phone_number: str, new_note: str) -> bool:
        """Update the phone number and note for an existing plate info."""
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE plate_info SET phone_number = ?, note = ? WHERE part1 = ? AND part2 = ?",
                (new_phone_number, new_note, part1, part2)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating plate info: {e}")
            return False

    @staticmethod
    def delete_plate_info(part1: str, part2: str) -> bool:
        """Delete a plate info from the database."""
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM plate_info WHERE part1 = ? AND part2 = ?",
                (part1, part2)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error deleting plate info: {e}")
            return False

    @staticmethod
    def filter_plate_info(part1_filter: str, part2_filter: str, phone_filter: str, search_mode: str = 'exact') -> list:
        """Filter plate info based on the given filters."""
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            # Prepare the query based on search mode
            if search_mode == 'exact':
                query = """
                    SELECT id, part1, part2, phone_number, note
                    FROM plate_info
                    WHERE part1 = ? AND part2 = ? AND phone_number = ?
                """
                params = (part1_filter, part2_filter, phone_filter)
            else:  # 'contains'
                query = """
                    SELECT id, part1, part2, phone_number, note
                    FROM plate_info
                    WHERE part1 LIKE ? OR part2 LIKE ? OR phone_number LIKE ?
                """
                params = (f"%{part1_filter}%", f"%{part2_filter}%", f"%{phone_filter}%")

            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error filtering plate info: {e}")
            return []

    @staticmethod
    def plate_exists(part1: str, part2: str) -> bool:
        """Check if the plate info already exists in the database."""
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM plate_info WHERE part1 = ? AND part2 = ?",
                (part1, part2)
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except Exception as e:
            logger.error(f"Error checking plate existence: {e}")
            return False

    @staticmethod
    def plate_and_phone_exists(part1: str, part2: str, phone_number: str) -> bool:
        """Check if both plate number and phone number are duplicated in the database."""
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM plate_info WHERE part1 = ? AND part2 = ? AND phone_number = ?",
                (part1, part2, phone_number)
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except Exception as e:
            logger.error(f"Error checking plate and phone existence: {e}")
            return False

    @staticmethod
    def plate_and_phone_note_exists(part1: str, part2: str, phone_number: str, note: str) -> bool:
        """Check if both plate number, phone number, and note are duplicated in the database."""
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM plate_info WHERE part1 = ? AND part2 = ? AND phone_number = ? AND note = ?",
                (part1, part2, phone_number, note)
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except Exception as e:
            logger.error(f"Error checking plate, phone, and note existence: {e}")
            return False
