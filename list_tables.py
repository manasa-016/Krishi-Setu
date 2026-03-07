from app.core.database import engine
from sqlalchemy import inspect

def list_tables():
    inspector = inspect(engine)
    print(f"Tables: {inspector.get_table_names()}")

if __name__ == "__main__":
    list_tables()
