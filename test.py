import random
import string
import sqlite3

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_unique_plate_infos(num):
    plate_infos = set()
    while len(plate_infos) < num:
        part1 = generate_random_string(3)
        part2 = generate_random_string(4)
        plate_infos.add((part1, part2))
    return list(plate_infos)

def generate_data(num_records=10000, db_path='database.db'):
    unique_plate_infos = generate_unique_plate_infos(num_records // 2)
    data = []
    for part1, part2 in unique_plate_infos:
        for _ in range(2):  # Create two records for each plate info with different phone numbers
            phone_number = ''.join(random.choices(string.digits, k=10))
            note = generate_random_string(10)
            data.append((part1, part2, phone_number, note))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS plate_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        part1 TEXT NOT NULL,
                        part2 TEXT NOT NULL,
                        phone_number TEXT NOT NULL,
                        note TEXT,
                        UNIQUE(part1, part2, phone_number))''')
    cursor.executemany("INSERT OR IGNORE INTO plate_info (part1, part2, phone_number, note) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_data()
