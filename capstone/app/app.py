import streamlit as st
st.set_page_config(page_title="CareerPilot", layout="wide")

from resume_optimizer import run_resume_optimizer
# from dashboard import run_dashboard
# from reports import run_reports

st.title("Career Pilot - Fuel your job search!")
# navigation bar
tab1, tab2, tab3 = st.tabs(["📝 Resume Optimizer", "👣 Job Tracker","📄 Generate Reports"])

with tab1:
    run_resume_optimizer()

# with tab2:
#     run_dashboard()

# with tab3:
#     run_reports()