from sqlalchemy import create_engine
from base import Base
from models import User, Chat  # Explicitly import models
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler("init_db_sync.log"), logging.StreamHandler()]
)

def init_db_sync():
    try:
        load_dotenv()
        logging.info("Initializing database synchronously...")
        logging.info(f"Metadata tables before create_all: {list(Base.metadata.tables.keys())}")
        DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://chatbot_user:your_secure_password@localhost:3306/chatbot_db").replace("aiomysql", "pymysql")
        engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(engine)
        logging.info("Database initialized successfully.")
        logging.info(f"Metadata tables after create_all: {list(Base.metadata.tables.keys())}")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    init_db_sync()