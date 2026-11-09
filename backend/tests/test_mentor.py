from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_mentor_chat():
    payload = {
        "message": "How do I prepare for technical interviews?",
        "context": {
            "target_role": "Backend Developer",
            "current_level": "beginner",
        },
    }
    response = client.post("/api/v1/mentor/chat", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "reply" in data
    assert len(data["reply"]) > 0
    assert len(data["actionable_tips"]) > 0
    assert len(data["suggested_prompts"]) > 0

