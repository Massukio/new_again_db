import sqlite3
from app.logger import logger

DATABASE_FILE = "database.db"

def get_connection():
    return sqlite3.connect(DATABASE_FILE)

def add_plate_info(part1: str, part2: str, phone_number: str, note: str) -> None:
    """Add a new plate info to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO plate_info (part1, part2, phone_number, note)
            VALUES (?, ?, ?, ?)
        ''', (part1.upper(), part2.upper(), phone_number, note))
        conn.commit()
        logger.info(f"Added plate info: {part1.upper()}-{part2.upper()} with phone number: {phone_number}")
    except sqlite3.IntegrityError as e:
        logger.warning(f"Failed to add plate info: {e}")
    finally:
        conn.close()

def get_all_plate_info() -> list:
    """Get all plate info from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT part1, part2, phone_number, note FROM plate_info')
    data = cursor.fetchall()
    conn.close()
    return [(f"{row[0]}-{row[1]}", row[2], row[3]) for row in data]

def update_plate_info(part1: str, part2: str, new_phone_number: str, new_note: str) -> None:
    """Update the phone number and note for an existing plate info."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT COUNT(*)
            FROM plate_info
            WHERE part1 = ? AND part2 = ? AND phone_number = ?
        ''', (part1.upper(), part2.upper(), new_phone_number))
        if cursor.fetchone()[0] > 0:
            raise sqlite3.IntegrityError("UNIQUE constraint failed: plate_info.part1, plate_info.part2, plate_info.phone_number")
        
        cursor.execute('''
            UPDATE plate_info
            SET phone_number = ?, note = ?
            WHERE part1 = ? AND part2 = ?
        ''', (new_phone_number, new_note, part1.upper(), part2.upper()))
        if cursor.rowcount > 0:
            conn.commit()
            logger.info(f"Updated plate info: {part1.upper()}-{part2.upper()}")
        else:
            logger.error("Plate info not found in the database.")
    except sqlite3.IntegrityError as e:
        logger.error(f"Failed to update plate info: {e}")
    finally:
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

def filter_plate_info(part1_filter: str, part2_filter: str, phone_filter: str, search_mode: str) -> list:
    """Filter plate info based on the given filters."""
    conn = get_connection()
    cursor = conn.cursor()
    if search_mode == "電話查詢":
        cursor.execute('''
            SELECT part1, part2, phone_number, note
            FROM plate_info
            WHERE phone_number LIKE ?
        ''', (f"%{phone_filter}%",))
    else:
        if part1_filter and part2_filter:
            cursor.execute('''
                SELECT part1, part2, phone_number, note
                FROM plate_info
                WHERE part1 LIKE ? AND part2 LIKE ?
            ''', (f"%{part1_filter}%", f"%{part2_filter}%"))
        elif part1_filter:
            cursor.execute('''
                SELECT part1, part2, phone_number, note
                FROM plate_info
                WHERE part1 LIKE ?
            ''', (f"%{part1_filter}%",))
        elif part2_filter:
            cursor.execute('''
                SELECT part1, part2, phone_number, note
                FROM plate_info
                WHERE part2 LIKE ?
            ''', (f"%{part2_filter}%",))
        else:
            cursor.execute('''
                SELECT part1, part2, phone_number, note
                FROM plate_info
            ''')
    data = cursor.fetchall()
    conn.close()
    return [(f"{row[0]}-{row[1]}", row[2], row[3]) for row in data]

def plate_exists(part1: str, part2: str) -> bool:
    """Check if the plate info already exists in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*)
        FROM plate_info
        WHERE part1 = ? AND part2 = ?
    ''', (part1.upper(), part2.upper()))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def plate_and_phone_exists(part1: str, part2: str, phone_number: str) -> bool:
    """Check if both plate number and phone number are duplicated in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*)
        FROM plate_info
        WHERE part1 = ? AND part2 = ? AND phone_number = ?
    ''', (part1.upper(), part2.upper(), phone_number))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists
