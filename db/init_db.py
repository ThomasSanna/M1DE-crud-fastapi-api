from sqlmodel import SQLModel
from db.database import engine
import models

def init_db():
    print("Creating database tables (if they don't exist)...")
    SQLModel.metadata.create_all(engine)
    print("Done.")

if __name__ == '__main__':
    init_db()
