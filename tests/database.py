from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test_social_media.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def set_up_database():
    with engine.connect() as conn:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS posts (
                            id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created_at TEXT DEFAULT current_timestamp
                            )'''))
        conn.execute(text('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            created_at TEXT DEFAULT current_timestamp
                            )'''))
        conn.commit()

def drop_database():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS posts"))
        conn.execute(text("DROP TABLE IF EXISTS users"))
        conn.commit()