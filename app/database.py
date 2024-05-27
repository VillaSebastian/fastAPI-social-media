import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./social_media.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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