import sqlite3

DATABASE_FILE = "database.db"

def query_by_plate(part1: str, part2: str) -> list:
    """Query the database by plate part1 and part2."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT part1, part2, phone_number, note
        FROM plate_info
        WHERE part1 = ? AND part2 = ?
    ''', (part1.upper(), part2.upper()))
    data = cursor.fetchall()
    conn.close()
    return [(f"{row[0]}-{row[1]}", row[2], row[3]) for row in data]

# Example usage
if __name__ == "__main__":
    part1 = "TZR"
    part2 = "L6QA"
    results = query_by_plate(part1, part2)
    for result in results:
        print(result)