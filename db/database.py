import sqlite3
from app.logger import logger

DATABASE_FILE = "database.db"

def get_connection():
    return sqlite3.connect(DATABASE_FILE)

def add_plate_info(part1: str, part2: str, phone_number: str) -> None:
    """Add a new plate info to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO plate_info (part1, part2, phone_number)
            VALUES (?, ?, ?)
        ''', (part1.upper(), part2.upper(), phone_number))
        conn.commit()
        logger.info(f"Added plate info: {part1.upper()}-{part2.upper()}")
    except sqlite3.IntegrityError:
        logger.error("Plate info already exists in the database.")
    finally:
        conn.close()

def get_all_plate_info() -> dict:
    """Get all plate info from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT part1, part2, phone_number FROM plate_info')
    data = cursor.fetchall()
    conn.close()
    return {f"{row[0]}-{row[1]}": {"phone_number": row[2]} for row in data}

def update_plate_info(part1: str, part2: str, new_phone_number: str) -> None:
    """Update the phone number for an existing plate info."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE plate_info
        SET phone_number = ?
        WHERE part1 = ? AND part2 = ?
    ''', (new_phone_number, part1.upper(), part2.upper()))
    if cursor.rowcount > 0:
        conn.commit()
        logger.info(f"Updated plate info: {part1.upper()}-{part2.upper()}")
    else:
        logger.error("Plate info not found in the database.")
    conn.close()

def delete_plate_info(part1: str, part2: str) -> None:
    """Delete a plate info from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM plate_info
        WHERE part1 = ? AND part2 = ?
    ''', (part1.upper(), part2.upper()))
    if cursor.rowcount > 0:
        conn.commit()
        logger.info(f"Deleted plate info: {part1.upper()}-{part2.upper()}")
    else:
        logger.error("Plate info not found in the database.")
    conn.close()

def filter_plate_info(part1_filter: str, part2_filter: str, phone_filter: str, search_mode: str) -> dict:
    """Filter plate info based on the given filters."""
    conn = get_connection()
    cursor = conn.cursor()
    if search_mode == "電話查詢":
        cursor.execute('''
            SELECT part1, part2, phone_number
            FROM plate_info
            WHERE phone_number LIKE ?
        ''', (f"%{phone_filter}%",))
    else:
        if part1_filter and part2_filter:
            cursor.execute('''
                SELECT part1, part2, phone_number
                FROM plate_info
                WHERE part1 LIKE ? AND part2 LIKE ?
            ''', (f"%{part1_filter}%", f"%{part2_filter}%"))
        elif part1_filter:
            cursor.execute('''
                SELECT part1, part2, phone_number
                FROM plate_info
                WHERE part1 LIKE ?
            ''', (f"%{part1_filter}%",))
        elif part2_filter:
            cursor.execute('''
                SELECT part1, part2, phone_number
                FROM plate_info
                WHERE part2 LIKE ?
            ''', (f"%{part2_filter}%",))
        else:
            cursor.execute('''
                SELECT part1, part2, phone_number
                FROM plate_info
            ''')
    data = cursor.fetchall()
    conn.close()
    return {f"{row[0]}-{row[1]}": {"phone_number": row[2]} for row in data}
