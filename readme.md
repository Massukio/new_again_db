# New Again Project

## Overview

This project is a car plate information management system built using Python and PyQt5. It allows users to add, view, update, and delete car plate information, including phone numbers and notes. The data is stored in an SQLite database.

## Features

- **Add Car Plate Information**: Add new car plate information with phone numbers and notes.
- **View All Information**: View all stored car plate information in a table format.
- **Update Information**: Update existing car plate information.
- **Delete Information**: Delete car plate information.
- **Search Functionality**: Search for car plate information by plate number or phone number.
- **Database Backup**: Backup the database to a specified location.

## Requirements

- Python 3.8+
- PyQt5
- SQLite3

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/new_again.git
    cd new_again
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Initialize the database:
    ```sh
    python db/initialize_db.py
    ```

2. Run the application:
    ```sh
    python start.py
    ```

## Project Structure

- `app/`: Contains the main application code.
  - `__init__.py`: Makes the directory a package.
  - `add_plate_dialog.py`: Dialog for adding car plate information.
  - `logger.py`: Configures logging for the application.
  - `main_ui.py`: Main UI setup for the application.
  - `table_view_handler.py`: Handles the table view operations.
- `db/`: Contains database-related scripts.
  - `__init__.py`: Makes the directory a package.
  - `database.py`: Database operations.
  - `initialize_db.py`: Script to initialize the database.
- `designer/`: Contains UI design files.
  - `add.ui`: UI design for adding car plate information.
  - `new_again.ui`: Main window UI design.
- `.vscode/`: Contains VS Code configuration files.
  - `settings.json`: VS Code settings.
  - `tasks.json`: VS Code tasks.
- `start.py`: Entry point for the application.
- `requirements.txt`: List of required packages.
- `.gitignore`: Git ignore file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Sukio Lin

## Acknowledgements

- PyQt5 Documentation
- SQLite Documentation
- Python Logging Documentation
- GitHub Copilot for assistance in code generation
- All contributors and users
