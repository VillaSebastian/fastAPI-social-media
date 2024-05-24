import sqlite3

def set_up_database():
    # Connect to the database (or create it if it doesn't exits)
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()

    # Create a table posts (if it doesn't exist)
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT current_timestamp
                    )''')

    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()