from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_assessment_flow():
    # 1. Start assessment
    start_payload = {
        "domain": "Python Backend",
        "target_role": "Backend Engineer",
        "skill_level": "beginner",
    }
    start_resp = client.post("/api/v1/assessments/start", json=start_payload)
    assert start_resp.status_code == 201
    start_data = start_resp.json()["data"]
    assessment_id = start_data["assessment_id"]
    assert start_data["total_questions"] > 0
    questions = start_data["questions"]

    # 2. Submit answers
    submit_payload = {
        "answers": [
            {"question_id": questions[0]["id"], "selected_option_id": "opt2"},
            {"question_id": questions[1]["id"], "selected_option_id": "opt2"},
        ]
    }
    submit_resp = client.post(
        f"/api/v1/assessments/{assessment_id}/submit", json=submit_payload
    )
    assert submit_resp.status_code == 200
    result_data = submit_resp.json()["data"]
    assert result_data["assessment_id"] == assessment_id
    assert "score_percentage" in result_data
    assert isinstance(result_data["skill_gaps"], list)

    # 3. Retrieve assessment result
    get_resp = client.get(f"/api/v1/assessments/{assessment_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["assessment_id"] == assessment_id

