import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
#from sqlalchemy.orm import Session
from openai import OpenAI
from docx import Document
from docx.shared import Pt
from fastapi.responses import FileResponse
from docx2pdf import convert
import uuid

#declare FastAPI
app = FastAPI()

# adding security feature to ensure only my streamlit frontend can send requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://career-pilot-fb35.onrender.com/"],  
    allow_credentials=True,
    allow_methods=["*"],                      
    allow_headers=["*"],                      
)
# open database connection for fastapi.
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db # yield the session so fastapi can use it.
#     finally:
#         db.close()

print("DEBUG >>>", os.getenv("OPENAI_API_KEY"))  

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables")
# Set your OpenAI API key
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
#os.getenv("OPENAI_API_KEY"),
)
#testing
class ResumeOptimizationRequest(BaseModel):
    resume: str
    job_description: str

@app.post("/optimize-resume")
def optimize_resume(payload: ResumeOptimizationRequest):
    prompt = f"""
You are a resume expert. Review the following resume and job description.
Based on the resume and job description below, generate a professionally formatted resume that is tailored to the job description. Use sections like Summary, Experience, Skills, and Education.


Resume:
{payload.resume}

Job Description:
{payload.job_description}

Suggestions:
"""

    try:
        response = client.responses.create(
            model = "gpt-4.1",  
            input = prompt
            #input = f"Resume: {payload.resume} + Job Description: {payload.job_description}"
            
        )

        tailored_resume = response.output_text
        #return {"recommendations": suggestions}
        # Generate DOCX file
        unique_id = uuid.uuid4().hex
        docx_filename = f"./generated_docs/resume_{unique_id}.docx"
        pdf_filename = f"./generated_docs/resume_{unique_id}.pdf"

        os.makedirs("generated_docs", exist_ok=True)

        doc = Document()
        style = doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)

        for line in tailored_resume.split('\n'):
            doc.add_paragraph(line)

        doc.save(docx_filename)

        # Convert to PDF (only works if Word is installed on machine)
        # try:
        #     convert(docx_filename, pdf_filename)
        #     return FileResponse(pdf_filename, media_type="application/pdf", filename="Tailored_Resume.pdf")
        # except Exception as pdf_error:
        #     print("PDF conversion failed, returning DOCX instead:", pdf_error)
        #     return FileResponse(docx_filename, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="Tailored_Resume.docx")


    except Exception as e:
        print("Error with your request:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
# # adds a new job application entry to the database
# @app.post("/jobs", response_model=schemas.JobApplicationResponse)
# def add_job(job: schemas.JobApplicationCreate, db: Session = Depends(get_db)):
#     return db_logic.create_job_app(db, job)

# # grab all the job applications
# @app.get("/jobs", response_model=list[schemas.JobApplicationResponse])
# def get_jobs(db: Session = Depends(get_db)):
#     return db_logic.get_all_jobs(db)

# # update a job application
# @app.put("/jobs/{job_id}", response_model=schemas.JobApplicationResponse)
# def update_job(job_id: int, job_update: schemas.JobApplicationUpdate, db: Session = Depends(get_db)):
#     updated_job = db_logic.update_job_app(db, job_id, job_update)
#     if not updated_job:
#         raise HTTPException(status_code=404, detail="Job not found")
#     return updated_job

# # delete a job application
# @app.delete("/jobs/{job_id}")
# def delete_job(job_id: int, db: Session = Depends(get_db)):
#     success = db_logic.delete_job_app(db, job_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Job not found")
#     return {"detail": "Job deleted"}

# # search database
# @app.get("/jobs/search/")
# def search_jobs(query: str, db: Session = Depends(get_db)):
#     return db.query(models.JobApplication).filter(
#         models.JobApplication.title.ilike(f"%{query}%")
#     ).all()
