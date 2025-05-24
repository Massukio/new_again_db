"""
This file initializes the database for the refactored implementation.
Standalone implementation that doesn't depend on the original codebase.
"""

import sqlite3
import os


def initialize_database(db_file="database.db"):
    """
    Initialize the database with the required schema.

    Args:
        db_file: Path to the database file
    """
    conn = sqlite3.connect(db_file)
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


def init_db(db_file="database.db"):
    """
    Initialize the database using the standalone implementation.
    This function can be called to ensure the database is properly set up.
    """
    initialize_database(db_file)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
