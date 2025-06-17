import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from capstone.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_job():
    response = client.post("/jobs", json={
        "title": "Test Engineer",
        "company": "Test Company",
        "job_description": "A test job.",
        "applied_on": "2025-06-14",
        "status": "Applied"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Engineer"

def test_get_jobs():
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_job():
    # create fake job
    post_res = client.post("/jobs", json={
        "title": "Temp Job",
        "company": "Temp Company",
        "job_description": "Temp description",
        "applied_on": "2025-06-14",
        "status": "Applied"
    })
    job_id = post_res.json()["id"]

    # Now update
    update_res = client.put(f"/jobs/{job_id}", json={
        "title": "Updated Job",
        "company": "Updated Company",
        "job_description": "Updated description",
        "applied_on": "2025-06-14",
        "status": "Interview"
    })
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Updated Job"

def test_delete_job():
    # Create a job to delete
    res = client.post("/jobs", json={
        "title": "Delete Me",
        "company": "Delete Co",
        "job_description": "Should be gone",
        "applied_on": "2025-06-14",
        "status": "Rejected"
    })
    job_id = res.json()["id"]

    delete_res = client.delete(f"/jobs/{job_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["detail"] == "Job deleted"
