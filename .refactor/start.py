#!/usr/bin/env python3
"""
Refactored start.py - Entry point for the New Again application.
This is a completely standalone implementation that doesn't depend on the original codebase.
"""

import os
import sys

# Get the absolute path to the current directory (.refactor)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to the Python path
sys.path.insert(0, current_dir)

# Import from the refactored implementation
from app.application import Application

if __name__ == "__main__":
    try:
        # Initialize and run the application
        app = Application()
        app.run()
    except Exception as e:
        # Print error message if application fails to start
        import traceback
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)
