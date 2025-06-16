from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./job_tracker.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# sessionmaker is used to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class, all models will inherit from this class structure.
Base = declarative_base()
