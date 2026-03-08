from app.core.database import engine
from sqlalchemy import text

def clear_version():
    with engine.connect() as connection:
        # Check if table exists
        try:
            connection.execute(text("DELETE FROM alembic_version"))
            connection.commit()
            print("Successfully cleared alembic_version table.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    clear_version()
