import os
import sqlite3

def create_database():
    # Remove existing database file if it exists
    db_path = '../database/people.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image BLOB NOT NULL
        )
    ''')

    # Insert multiple sample data
    people_data = [
        ('Niko', 'sample.png'),
        ('Ion', 'ion.png'),
        ('Iezhen', 'iezhen.png'),
        ('Alice', 'alice.png'),
        ('Bob', 'bob.png'),
    ]

    for name, image_file in people_data:
        try:
            with open(image_file, 'rb') as f:
                image_data = f.read()
            cursor.execute("INSERT INTO people (name, image) VALUES (?, ?)", (name, image_data))
        except FileNotFoundError:
            print(f"File not found: {image_file}")

    connection.commit()
    connection.close()
    print("Database created and sample data inserted successfully!")

if __name__ == '__main__':
    create_database()