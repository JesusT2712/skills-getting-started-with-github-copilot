import json
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Ensure known activity exists
    assert "Soccer Team" in data


def test_signup_and_unregister_cycle():
    activity = "Soccer Team"
    email = "test.student@example.com"

    # Ensure email not already in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Verify participant was added
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data = resp2.json()
    assert email in data[activity]["participants"]

    # Unregister
    resp3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp3.status_code == 200
    assert "Unregistered" in resp3.json()["message"]

    # Verify removed
    resp4 = client.get("/activities")
    assert resp4.status_code == 200
    data2 = resp4.json()
    assert email not in data2[activity]["participants"]
