import uuid
from typing import List, Dict, Optional
from app.schemas.mentor import (
    MentorChatRequest,
    MentorChatResponse,
    MentorContext,
)


class MentorService:
    @staticmethod
    def chat(request: MentorChatRequest) -> MentorChatResponse:
        conv_id = request.conversation_id or f"chat-{uuid.uuid4().hex[:8]}"
        msg_lower = request.message.lower()
        context = request.context or MentorContext()
        role = context.target_role or "Software Engineer"

        # Context-aware prototype response generator
        if "interview" in msg_lower or "interviewing" in msg_lower:
            reply = (
                f"For {role} interviews, focus on a 3-part strategy: "
                "1. Data structures & algorithms (focus on hash maps, trees, and two-pointer patterns). "
                "2. System design fundamentals (caching, database indexing, REST semantics). "
                "3. Behavioral answers formatted in the STAR method (Situation, Task, Action, Result)."
            )
            actionable_tips = [
                "Solve 2 medium LeetCode/HackerRank problems daily focusing on patterns.",
                "Conduct a mock interview with a peer or record yourself explaining a project.",
                "Prepare 3 deep-dive stories about challenging bugs you solved.",
            ]
            suggested_prompts = [
                "What system design questions are asked for junior/mid backend roles?",
                "Can you review my STAR format answer?",
                "How do I explain my projects clearly on a resume?",
            ]

        elif "resume" in msg_lower or "cv" in msg_lower:
            reply = (
                f"When tailoring your resume for {role} positions, prioritize quantifiable impact over task lists. "
                "Instead of 'Created REST APIs', write 'Architected 8 FastAPI endpoints with Pydantic validation, decreasing payload parsing latency by 25%'."
            )
            actionable_tips = [
                "Use the XYZ formula: Accomplished [X], as measured by [Y], by doing [Z].",
                "Keep your tech stack keywords prominent at the top for ATS scanners.",
                "Link live demos and clean GitHub repositories with documented READMEs.",
            ]
            suggested_prompts = [
                "How should I format bullet points for my personal project?",
                "Should I include certifications on my resume?",
                "Can you check if my resume tech stack matches my target role?",
            ]

        elif "roadmap" in msg_lower or "start" in msg_lower or "learn" in msg_lower:
            reply = (
                f"To accelerate your progress toward {role}, break down your learning into 2-week milestones. "
                "Always build a small functional project after learning each concept (e.g., build a CRUD API before moving to caching)."
            )
            actionable_tips = [
                "Follow your AVENTIQ personalized roadmap one milestone at a time.",
                "Commit code to GitHub daily to build consistency and an authentic portfolio.",
                "Take the diagnostic skill assessment to highlight your exact gap areas.",
            ]
            suggested_prompts = [
                "What beginner project should I build for backend engineering?",
                "How many hours per week should I study?",
                "How do I choose between PostgreSQL and MongoDB?",
            ]

        else:
            reply = (
                f"I'm your AVENTIQ AI Career Mentor. I'm here to support your transition into {role}. "
                "Whether you need guidance on technical skill gaps, interview prep, project ideas, or resume tailoring, ask away!"
            )
            actionable_tips = [
                "Start with the Skill Assessment to calibrate your starting level.",
                "Generate your personalized roadmap under the Roadmaps section.",
                "Ask me any specific technical or career question whenever you feel stuck.",
            ]
            suggested_prompts = [
                "How can I prepare for technical interviews?",
                "What are the most in-demand skills for backend developers?",
                "How should I structure my GitHub portfolio?",
            ]

        return MentorChatResponse(
            conversation_id=conv_id,
            reply=reply,
            actionable_tips=actionable_tips,
            suggested_prompts=suggested_prompts,
        )

