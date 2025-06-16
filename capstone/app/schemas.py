from pydantic import BaseModel
from datetime import datetime

# sets the format of the class so data being sent back and forth is validated
class JobApplicationCreate(BaseModel):
    title: str
    company: str
    job_description: str
    status: str
    applied_on: datetime

# sets the format of the class so data being sent back and forth is validated
class JobApplicationUpdate(BaseModel):
    title: str
    company: str
    job_description: str
    status: str
    applied_on: datetime


# sets the format of the class so data being sent back and forth is validated
class JobApplicationResponse(BaseModel):
    id: int
    title: str
    company: str
    job_description: str
    status: str
    applied_on: datetime

    class Config:
        orm_mode = True