from sqlalchemy.ext.asyncio import AsyncEngine
from database import engine
from base import Base
from models import User, Chat  # Explicitly import models
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler("init_db.log"), logging.StreamHandler()]
)

async def init_db():
    try:
        logging.info("Initializing database...")
        logging.info(f"Metadata tables before create_all: {list(Base.metadata.tables.keys())}")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logging.info("Database initialized successfully.")
        logging.info(f"Metadata tables after create_all: {list(Base.metadata.tables.keys())}")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())