from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

import models
import schemas

# creates a new job application entry for the database
def create_job_app(db: Session, job_app_data: schemas.JobApplicationCreate):
    new_job_app = models.JobApplication(**job_app_data.dict()) # turns job_app_data into a dictionary. 
    db.add(new_job_app)
    db.commit()
    db.refresh(new_job_app) 
    return new_job_app

#grab all jobs from database
def get_all_jobs(db: Session):
    return db.query(models.JobApplication).all()

#delete a job application
def delete_job_app(db: Session, job_id: int):
    job = db.query(models.JobApplication).get(job_id)
    if job:
        db.delete(job)
        db.commit()
    return JSONResponse(content={"message": "Job deleted"})
    

# update a job application
def update_job_app(db: Session, job_id: int, updated_data: schemas.JobApplicationUpdate):
    job = db.query(models.JobApplication).get(job_id)
    if not job:
        return None
    
    for key, value in updated_data.dict().items():
        setattr(job, key, value)
    
    db.commit()
    db.refresh(job)
    return job
