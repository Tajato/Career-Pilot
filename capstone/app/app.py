import streamlit as st
st.set_page_config(page_title="CareerPilot", layout="wide")

from resume_optimizer import run_resume_optimizer
from dashboard import run_dashboard


tab1, tab2 = st.tabs(["📝 Resume Optimizer", "📊 Job Tracker"])

with tab1:
    run_resume_optimizer()

with tab2:
    run_dashboard()