# from sqlalchemy import Column, Integer, String, Text, DateTime

# from database import Base
# from datetime import datetime
# from database import engine

# #inherit from base calls tells Python to define a table with this structure in the database
# class JobApplication(Base):
#     __tablename__ = "job_applications" #database table name

#     #all the columns
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     company = Column(String, nullable=False)
#     job_description = Column(Text, nullable=False)
#     status = Column(Text, nullable=False)
#     applied_on = Column(DateTime, default=datetime.utcnow)


# Base.metadata.create_all(bind=engine)
