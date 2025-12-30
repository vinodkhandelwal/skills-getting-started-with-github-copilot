from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

def setup_function():
    global _activities_backup
    _activities_backup = copy.deepcopy(activities)

def teardown_function():
    activities.clear()
    activities.update(copy.deepcopy(_activities_backup))

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Basketball"
    email = "tester@example.com"

    # Ensure clean start for this email
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_un = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp_un.status_code == 200
    assert email not in activities[activity]["participants"]

def test_unregister_nonexistent():
    activity = "Tennis Club"
    email = "nobody@example.com"

    # Ensure email is not registered
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 400
