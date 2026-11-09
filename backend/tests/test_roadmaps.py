from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_and_fetch_roadmap():
    # 1. Generate roadmap
    payload = {
        "target_role": "Backend Engineer",
        "current_level": "beginner",
        "hours_per_week": 15,
        "background": "Student with basic Python knowledge",
        "preferred_learning_style": "hands_on",
    }
    response = client.post("/api/v1/roadmaps/generate", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    roadmap = data["data"]
    roadmap_id = roadmap["id"]
    assert roadmap["target_role"] == "Backend Engineer"
    assert len(roadmap["phases"]) > 0
    assert roadmap["total_milestones"] > 0
    assert roadmap["completed_milestones"] == 0

    # 2. Fetch the generated roadmap
    fetch_resp = client.get(f"/api/v1/roadmaps/{roadmap_id}")
    assert fetch_resp.status_code == 200
    assert fetch_resp.json()["data"]["id"] == roadmap_id

    # 3. Complete the first milestone
    first_milestone_id = roadmap["phases"][0]["milestones"][0]["id"]
    update_resp = client.patch(
        f"/api/v1/roadmaps/{roadmap_id}/milestones/{first_milestone_id}",
        json={"is_completed": True},
    )
    assert update_resp.status_code == 200
    updated_roadmap = update_resp.json()["data"]
    assert updated_roadmap["completed_milestones"] == 1


def test_get_nonexistent_roadmap():
    resp = client.get("/api/v1/roadmaps/nonexistent-id")
    assert resp.status_code == 404

