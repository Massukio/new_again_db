"""
This file initializes the database for the refactored implementation.
Reuses the original initialization logic to ensure compatibility.
"""

# Import original code
from db.initialize_db import initialize_database


def init_db():
    """
    Initialize the database using the original initialization logic.
    This function can be called to ensure the database is properly set up.
    """
    initialize_database()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
