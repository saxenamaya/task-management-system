from sqlalchemy import create_engine, text
from app.db.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS task_assignments"))

print("task_assignments table removed")
