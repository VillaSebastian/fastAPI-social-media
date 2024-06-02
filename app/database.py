from sqlalchemy import create_engine, text, event
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

# Ensure that foreign keys are enabled for each connection
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def set_up_database():
    with engine.connect() as conn:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            created_at TEXT DEFAULT current_timestamp
                            )'''))
        conn.execute(text('''CREATE TABLE IF NOT EXISTS posts (
                            id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created_at TEXT DEFAULT current_timestamp,
                            user_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id)
                                REFERENCES users (id)
                                    ON DELETE CASCADE
                            )'''))
        conn.commit()