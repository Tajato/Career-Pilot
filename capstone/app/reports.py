import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime

#Generates reports for users
def run_reports():
    st.title("📄 Generate a Report")
    API_URL = "https://career-pilot-backend-0dfi.onrender.com"

    report_type = st.selectbox(
        "Choose a report type",
        ["All Applications", "Applied This Month", "By Status", "Timeline View"]
    )

    if st.button("Generate Report"):
        try:
            report_response = requests.get(f"{API_URL}/jobs")
            if report_response.status_code == 200:
                report_data = report_response.json()
                df = pd.DataFrame(report_data)

                df['applied_on'] = pd.to_datetime(df['applied_on'])
                st.markdown(f"### 📝 Report: {report_type} (Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

                if report_type == "All Applications":
                    st.dataframe(df[["title", "company", "status", "applied_on", "job_description"]])

                elif report_type == "Applied This Month":
                    this_month = df[df['applied_on'].dt.month == datetime.now().month]
                    st.dataframe(this_month[["title", "company", "status", "applied_on"]])

                elif report_type == "By Status":
                    st.dataframe(df["status"].value_counts())

                elif report_type == "Timeline View":
                    df_sorted = df.sort_values("applied_on", ascending=True)
                    st.dataframe(df_sorted[["applied_on", "title", "company", "status"]])

                # Allow export
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download Report as CSV", data=csv, file_name=f"{report_type.replace(' ', '_').lower()}_report.csv", mime="text/csv")

            else:
                st.error("❌ Could not fetch job data.")
        except Exception as e:
            st.error(f"Report generation error: {e}")
