from app.core.database import engine
from sqlalchemy import inspect

def check_columns():
    inspector = inspect(engine)
    for table in ["farms", "shops"]:
        print(f"Table: {table}")
        for column in inspector.get_columns(table):
            print(f"  Column: {column['name']}, Type: {column['type']}")

if __name__ == "__main__":
    check_columns()
