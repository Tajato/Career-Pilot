import requests

url = "http://127.0.0.1:8000/optimize-resume"
payload = {
    "resume": """
Software Engineer with 3 years of experience building full-stack applications using Python, FastAPI, and JavaScript. Worked on internal tools and automated reporting dashboards.
""",
    "job_description": """
We're looking for a Backend Developer with experience in building scalable APIs using FastAPI and deploying them to cloud services. Must understand database design, REST principles, and team collaboration using Git.
"""
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Response:\n", response.json())
