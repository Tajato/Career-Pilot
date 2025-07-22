import streamlit as st
import requests
from datetime import datetime
import pdfplumber

# Page that provide resume recommendations
def run_resume_optimizer():
    st.header("Resume Optimizer")
    col1, col2 = st.columns(2)
    with col1:
        resume_option = st.radio("Choose a upload method:", ["Upload PDF", "Paste Text"])
        resume_text = ""
        if resume_option == "Upload PDF":
            uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")
        if uploaded_file:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    resume_text += page.extract_text()
        else:
            resume_text = st.text_area("Paste your resume text here:")
    with col2:
        job_description = st.text_area("Paste the job description here:", height=400)
    if st.button("Optimize My Resume"):
        if resume_text and job_description:
            with st.spinner("Analyzing with AI..."):
                response = requests.post("https://career-pilot-backend-0dfi.onrender.com/optimize-resume", json={
                "resume": resume_text,
                "job_description": job_description
            })
            if response.status_code == 200:
                 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                 filename = f"Tahj_Gordon_Resume_{timestamp}.docx"
                 st.success("Done! Click below to download:")
                 st.download_button("Download Resume", response.content, file_name=filename)
            else:
                st.error("Something went wrong.")
    else:
        st.warning("Please provide both resume and job description.")
