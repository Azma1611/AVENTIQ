import sys
from pathlib import Path
from fastapi import HTTPException

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import health_check
from app.api.v1.endpoints.roadmaps import generate_roadmap, get_roadmap, update_milestone_status
from app.api.v1.endpoints.assessments import start_assessment, submit_assessment, get_assessment_result
from app.api.v1.endpoints.mentor import chat_with_mentor
from app.api.v1.endpoints.resources import list_resources
from app.schemas.roadmap import RoadmapCreateRequest, MilestoneUpdateRequest
from app.schemas.assessment import AssessmentStartRequest, AssessmentSubmitRequest, AssessmentAnswerItem
from app.schemas.mentor import MentorChatRequest, MentorContext


def test_health():
    res = health_check()
    assert res["status"] == "healthy"
    assert res["app"] == "AVENTIQ API"


def test_roadmaps():
    req = RoadmapCreateRequest(
        target_role="Backend Engineer",
        current_level="beginner",
        hours_per_week=12,
        background="CS student",
    )
    resp = generate_roadmap(req)
    assert resp.success is True
    rm = resp.data
    assert rm.target_role == "Backend Engineer"
    assert len(rm.phases) > 0
    assert rm.completed_milestones == 0

    # Fetch
    fetched = get_roadmap(rm.id)
    assert fetched.data.id == rm.id

    # Update milestone
    first_ms = rm.phases[0].milestones[0].id
    updated = update_milestone_status(rm.id, first_ms, MilestoneUpdateRequest(is_completed=True))
    assert updated.data.completed_milestones == 1

    # 404 test
    try:
        get_roadmap("invalid-id")
        assert False, "Should raise 404"
    except HTTPException as e:
        assert e.status_code == 404


def test_assessments():
    start_req = AssessmentStartRequest(domain="Python Backend", target_role="Backend Developer")
    start_resp = start_assessment(start_req)
    assert start_resp.success is True
    asmt = start_resp.data
    assert len(asmt.questions) > 0

    # Submit
    submit_req = AssessmentSubmitRequest(
        answers=[
            AssessmentAnswerItem(question_id=asmt.questions[0].id, selected_option_id="opt2"),
            AssessmentAnswerItem(question_id=asmt.questions[1].id, selected_option_id="opt2"),
        ]
    )
    result_resp = submit_assessment(asmt.assessment_id, submit_req)
    assert result_resp.success is True
    result = result_resp.data
    assert result.assessment_id == asmt.assessment_id
    assert len(result.skill_gaps) > 0

    # Retrieve
    fetch_result = get_assessment_result(asmt.assessment_id)
    assert fetch_result.data.assessment_id == asmt.assessment_id


def test_mentor():
    chat_req = MentorChatRequest(
        message="What are the best interview tips for backend roles?",
        context=MentorContext(target_role="Backend Engineer"),
    )
    chat_resp = chat_with_mentor(chat_req)
    assert chat_resp.success is True
    assert len(chat_resp.data.reply) > 0
    assert len(chat_resp.data.actionable_tips) > 0
    assert len(chat_resp.data.suggested_prompts) > 0


def test_resources():
    resp = list_resources(skill="FastAPI", type=None, difficulty=None, search=None)
    assert resp.success is True
    assert resp.data.total >= 1

    search_resp = list_resources(skill=None, type=None, difficulty=None, search="Docker")
    assert search_resp.success is True
    assert search_resp.data.total >= 1


def run_all():
    print("=" * 65)
    print(" AVENTIQ BACKEND PROTOTYPE TEST SUITE")
    print("=" * 65)

    tests = [
        ("Health Check Endpoint", test_health),
        ("Personalized Roadmap (Generate, Fetch, Milestone Toggle, 404)", test_roadmaps),
        ("Skill Assessment (Start, Answer Submission, Gap Analysis)", test_assessments),
        ("AI Career Mentor (Contextual Advice & Follow-up Prompts)", test_mentor),
        ("Curated Learning Resources (Catalog Filtering & Search)", test_resources),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f" [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f" [FAIL] {name}: {e}")
            failed += 1

    print("=" * 65)
    print(f" Summary: {passed} passed, {failed} failed out of {len(tests)} tests.")
    print("=" * 65)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_all()
