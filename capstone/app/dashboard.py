import streamlit as st
import requests
from datetime import date, datetime


#st.set_page_config(page_title="Job Tracker", layout="wide")

def run_dashboard():
    st.title("Job Application Tracker")
    API_URL = "http://localhost:8000"

    search_query = st.text_input("🔍 Search by job title or company")

    st.subheader("➕ Add a New Job Application")
    with st.form("job_form"):
        title = st.text_input("Job Title")
        company = st.text_input("Company")
        description = st.text_area("Job Description")
        applied_on = st.date_input("Date Applied", value=date.today())
        status = st.selectbox("Application Status", ["Applied", "Interview", "Offer", "Rejected"])
        submitted = st.form_submit_button("Add Job")

    if submitted:
        payload = {
            "title": title,
            "company": company,
            "job_description": description,
            "applied_on": applied_on.isoformat(),
            "status": status
        }
        res = requests.post(f"{API_URL}/jobs", json=payload)
        if res.status_code == 200:
            st.success("✅ Job application added!")
            st.rerun()
        else:
            st.error(f"❌ Failed to add job: {res.text}")

    st.subheader("📊 Your Job Applications")

    try:
        response = requests.get(f"{API_URL}/jobs")
        if response.status_code == 200:
            job_data = response.json()

            if search_query:
                job_data = [
                    job for job in job_data
                    if search_query.lower() in job["title"].lower()
                    or search_query.lower() in job["company"].lower()
                ]

            if job_data:
                for job in job_data:
                    job_id = job["id"]
                    edit_key = f"edit_{job_id}"
                    if edit_key not in st.session_state:
                        st.session_state[edit_key] = False

                    with st.expander(f"{job['title']} at {job['company']}"):
                        st.markdown(f"**Status:** {job['status']}")
                        st.markdown(f"**Applied On:** {job['applied_on']}")
                        st.markdown(f"**Description:**\n{job['job_description']}")

                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button("✏️ Edit", key=f"edit_btn_{job_id}"):
                                st.session_state[edit_key] = not st.session_state[edit_key]

                        with col2:
                            if st.button("🗑️ Delete", key=f"delete_btn_{job_id}"):
                                res = requests.delete(f"{API_URL}/jobs/{job_id}")
                                if res.status_code == 200:
                                    st.success("🗑️ Job deleted!")
                                    st.rerun()
                                else:
                                    st.error("❌ Deletion failed.")

                        if st.session_state[edit_key]:
                            with st.form(f"edit_form_{job_id}"):
                                new_title = st.text_input("Edit Title", value=job["title"], key=f"title_{job_id}")
                                new_company = st.text_input("Edit Company", value=job["company"], key=f"company_{job_id}")
                                new_description = st.text_area("Edit Description", value=job["job_description"], key=f"desc_{job_id}")
                                new_applied = st.date_input("Edit Date", value=datetime.fromisoformat(job["applied_on"]).date(), key=f"date_{job_id}")
                                new_status = st.selectbox(
                                    "Edit Status",
                                    ["Applied", "Interview", "Offer", "Rejected"],
                                    index=["Applied", "Interview", "Offer", "Rejected"].index(job["status"]),
                                    key=f"status_{job_id}"
                                )
                                if st.form_submit_button("Save Changes"):
                                    update_payload = {
                                        "title": new_title,
                                        "company": new_company,
                                        "job_description": new_description,
                                        "applied_on": new_applied.isoformat(),
                                        "status": new_status
                                    }
                                    res = requests.put(f"{API_URL}/jobs/{job_id}", json=update_payload)
                                    if res.status_code == 200:
                                        st.success("✅ Updated!")
                                        st.session_state[edit_key] = False
                                        st.rerun()
                                    else:
                                        st.error("❌ Update failed.")
            else:
                st.info("No job applications found.")
        else:
            st.error("Unable to fetch job applications.")
    except Exception as e:
        st.error(f"Error: {e}")
