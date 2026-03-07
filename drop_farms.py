from app.core.database import engine
from sqlalchemy import text

def drop_farms():
    with engine.connect() as connection:
        try:
            connection.execute(text("DROP TABLE IF EXISTS farms"))
            connection.commit()
            print("Successfully dropped farms table.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    drop_farms()
