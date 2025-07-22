# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# # postgre database URL
# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


# if not SQLALCHEMY_DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set in environment variables.")

# engine = create_engine(
#    SQLALCHEMY_DATABASE_URL
# )

# # sessionmaker is used to talk to the database
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class, all models will inherit from this class structure.
# Base = declarative_base()
