#!/usr/bin/env python3
"""
Refactored start.py - Entry point for the New Again application.
This implements the requirements specified in the refactoring specification:
- Preserve root folder code integrity
- Reference original code without modifying it
- Maintain identical UI layout and components
"""

import os
import sys

# Get the absolute path to the root directory
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the root directory to the Python path to import original modules
sys.path.insert(0, root_dir)

# Add the refactored directory to the Python path
refactored_dir = os.path.join(root_dir, '.refactor')
sys.path.insert(0, refactored_dir)

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
