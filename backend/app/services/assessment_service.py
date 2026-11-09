import uuid
from typing import Dict, List, Optional
from app.schemas.assessment import (
    AssessmentStartRequest,
    AssessmentStartResponse,
    AssessmentQuestion,
    QuestionOption,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
    SkillGap,
)

# In-memory bank of questions (domain -> list of questions with correct answer metadata)
_QUESTION_BANK = [
    {
        "id": "q1",
        "domain": "backend",
        "category": "Async Programming",
        "text": "In Python's asyncio, what is the key difference between 'async def' and a normal 'def' function?",
        "options": [
            {"id": "opt1", "text": "async def functions run on a separate OS thread automatically."},
            {"id": "opt2", "text": "async def functions return a coroutine object and require 'await' or an event loop to execute."},
            {"id": "opt3", "text": "async def functions can only use global variables."},
            {"id": "opt4", "text": "There is no difference; it is purely a syntax hint."},
        ],
        "correct_option_id": "opt2",
        "skill": "AsyncIO",
    },
    {
        "id": "q2",
        "domain": "backend",
        "category": "REST API Architecture",
        "text": "Which HTTP status code is most appropriate for a request that succeeded and resulted in a new resource being created?",
        "options": [
            {"id": "opt1", "text": "200 OK"},
            {"id": "opt2", "text": "201 Created"},
            {"id": "opt3", "text": "204 No Content"},
            {"id": "opt4", "text": "301 Moved Permanently"},
        ],
        "correct_option_id": "opt2",
        "skill": "REST Architecture",
    },
    {
        "id": "q3",
        "domain": "backend",
        "category": "Databases & Indexing",
        "text": "Why would adding a B-Tree index on a high-cardinality column improve SELECT query performance?",
        "options": [
            {"id": "opt1", "text": "It compresses the table data into RAM."},
            {"id": "opt2", "text": "It changes table storage from disk to Redis."},
            {"id": "opt3", "text": "It allows logarithmic O(log N) lookup instead of a full table scan O(N)."},
            {"id": "opt4", "text": "It locks the table so concurrent writes are forbidden."},
        ],
        "correct_option_id": "opt3",
        "skill": "Database Optimization",
    },
    {
        "id": "q4",
        "domain": "backend",
        "category": "API Security",
        "text": "What is the primary vulnerability prevented by using parameterized SQL queries or ORMs?",
        "options": [
            {"id": "opt1", "text": "Cross-Site Scripting (XSS)"},
            {"id": "opt2", "text": "SQL Injection (SQLi)"},
            {"id": "opt3", "text": "Distributed Denial of Service (DDoS)"},
            {"id": "opt4", "text": "Man-in-the-Middle (MITM)"},
        ],
        "correct_option_id": "opt2",
        "skill": "Security Best Practices",
    },
]

# In-memory store for active assessments and results
_ACTIVE_ASSESSMENTS: Dict[str, dict] = {}
_COMPLETED_RESULTS: Dict[str, AssessmentResultResponse] = {}


class AssessmentService:
    @staticmethod
    def start_assessment(request: AssessmentStartRequest) -> AssessmentStartResponse:
        assessment_id = f"asmt-{uuid.uuid4().hex[:8]}"

        # Select relevant questions
        selected = _QUESTION_BANK  # For prototype, provide core backend diagnostic questions
        questions_for_client = [
            AssessmentQuestion(
                id=q["id"],
                text=q["text"],
                category=q["category"],
                options=[QuestionOption(id=opt["id"], text=opt["text"]) for opt in q["options"]],
                difficulty="medium",
            )
            for q in selected
        ]

        _ACTIVE_ASSESSMENTS[assessment_id] = {
            "domain": request.domain,
            "questions": selected,
        }

        return AssessmentStartResponse(
            assessment_id=assessment_id,
            domain=request.domain,
            total_questions=len(questions_for_client),
            questions=questions_for_client,
        )

    @staticmethod
    def submit_assessment(
        assessment_id: str, request: AssessmentSubmitRequest
    ) -> Optional[AssessmentResultResponse]:
        active = _ACTIVE_ASSESSMENTS.get(assessment_id)
        if not active:
            # Fallback for testing if not previously stored
            active = {"domain": "General Software Engineering", "questions": _QUESTION_BANK}

        answer_map = {ans.question_id: ans.selected_option_id for ans in request.answers}
        total_q = len(active["questions"])
        correct_count = 0
        skill_scores: Dict[str, List[bool]] = {}

        for q in active["questions"]:
            q_id = q["id"]
            skill = q.get("skill", "General")
            is_correct = answer_map.get(q_id) == q["correct_option_id"]
            if is_correct:
                correct_count += 1
            skill_scores.setdefault(skill, []).append(is_correct)

        score_percentage = round((correct_count / max(1, total_q)) * 100, 1)

        strengths: List[str] = []
        gaps: List[SkillGap] = []

        for skill, results in skill_scores.items():
            skill_pct = round((sum(results) / len(results)) * 100)
            if skill_pct >= 80:
                strengths.append(skill)
                status = "proficient"
                recommendations = [f"Strong mastery in {skill}. Continue with advanced system design projects."]
            elif skill_pct >= 50:
                status = "needs_practice"
                recommendations = [f"Practice hands-on coding exercises in {skill}."]
            else:
                status = "critical_gap"
                recommendations = [f"Prioritize foundational study and tutorials for {skill}."]

            gaps.append(
                SkillGap(
                    skill_name=skill,
                    proficiency_score=skill_pct,
                    status=status,
                    recommendations=recommendations,
                )
            )

        recommended_topics = [
            f"Review {gap.skill_name} core concepts"
            for gap in gaps
            if gap.status in ("needs_practice", "critical_gap")
        ]

        result = AssessmentResultResponse(
            assessment_id=assessment_id,
            domain=active["domain"],
            score_percentage=score_percentage,
            strengths=strengths,
            skill_gaps=gaps,
            recommended_roadmap_topics=recommended_topics,
        )

        _COMPLETED_RESULTS[assessment_id] = result
        return result

    @staticmethod
    def get_result(assessment_id: str) -> Optional[AssessmentResultResponse]:
        return _COMPLETED_RESULTS.get(assessment_id)

