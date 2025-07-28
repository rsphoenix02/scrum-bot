# reset_db.py
from app.db.engine import engine
from app.db.base import Base
from app.models import user, channel, standup

# Step 1: Drop all tables
Base.metadata.drop_all(bind=engine)

# Step 2: Recreate all tables
Base.metadata.create_all(bind=engine)

# Step 3: Reset alembic version to "base"
from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("DELETE FROM alembic_version"))
    conn.commit()

