import sqlite3


def create_database():
    connection = sqlite3.connect("students.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        year_level INTEGER NOT NULL
    )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()