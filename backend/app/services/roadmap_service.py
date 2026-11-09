import uuid
from typing import Dict, Optional, List
from app.schemas.roadmap import (
    RoadmapCreateRequest,
    RoadmapResponse,
    RoadmapPhase,
    RoadmapMilestone,
    RoadmapResource,
)

# In-memory store for prototype persistence
_ROADMAPS_DB: Dict[str, RoadmapResponse] = {}


class RoadmapService:
    @staticmethod
    def generate_roadmap(request: RoadmapCreateRequest) -> RoadmapResponse:
        roadmap_id = f"rm-{uuid.uuid4().hex[:8]}"
        role_lower = request.target_role.lower()

        # Build dynamic curriculum based on role
        if "frontend" in role_lower or "react" in role_lower or "ui" in role_lower:
            phases = RoadmapService._generate_frontend_phases(request.current_level)
            summary = f"Structured path to master Frontend Development as a {request.current_level} targeting '{request.target_role}'."
        elif "data" in role_lower or "ai" in role_lower or "machine learning" in role_lower:
            phases = RoadmapService._generate_data_phases(request.current_level)
            summary = f"Comprehensive roadmap for Data Science & AI engineering targeting '{request.target_role}'."
        else:
            # Default to backend / full-stack engineering
            phases = RoadmapService._generate_backend_phases(request.current_level)
            summary = f"Practical roadmap to master Backend Engineering targeting '{request.target_role}'."

        total_milestones = sum(len(phase.milestones) for phase in phases)
        estimated_weeks = max(4, round((total_milestones * 12) / request.hours_per_week))

        roadmap = RoadmapResponse(
            id=roadmap_id,
            target_role=request.target_role,
            current_level=request.current_level,
            estimated_weeks=estimated_weeks,
            summary=summary,
            phases=phases,
            total_milestones=total_milestones,
            completed_milestones=0,
        )

        _ROADMAPS_DB[roadmap_id] = roadmap
        return roadmap

    @staticmethod
    def get_roadmap(roadmap_id: str) -> Optional[RoadmapResponse]:
        return _ROADMAPS_DB.get(roadmap_id)

    @staticmethod
    def update_milestone_status(
        roadmap_id: str, milestone_id: str, is_completed: bool
    ) -> Optional[RoadmapResponse]:
        roadmap = _ROADMAPS_DB.get(roadmap_id)
        if not roadmap:
            return None

        found = False
        for phase in roadmap.phases:
            for ms in phase.milestones:
                if ms.id == milestone_id:
                    ms.is_completed = is_completed
                    found = True
                    break
            if found:
                break

        if not found:
            return None

        # Recalculate completed count
        completed_count = sum(
            1 for p in roadmap.phases for m in p.milestones if m.is_completed
        )
        roadmap.completed_milestones = completed_count
        _ROADMAPS_DB[roadmap_id] = roadmap
        return roadmap

    @staticmethod
    def _generate_backend_phases(level: str) -> List[RoadmapPhase]:
        return [
            RoadmapPhase(
                phase_number=1,
                title="Phase 1: Backend Core & Programming Foundations",
                description="Deep dive into Python/backend language semantics, async programming, and data structures.",
                milestones=[
                    RoadmapMilestone(
                        id="be-m1",
                        title="Master Python Data Structures & Asynchronous I/O",
                        description="Understand lists, dicts, generators, asyncio, and typing.",
                        estimated_hours=12,
                        skills_covered=["Python", "AsyncIO", "Type Hinting"],
                        resources=[
                            RoadmapResource(
                                title="Official Python Async Documentation",
                                url="https://docs.python.org/3/library/asyncio.html",
                                type="documentation",
                            ),
                            RoadmapResource(
                                title="Real Python: Async IO in Python",
                                url="https://realpython.com/async-io-python/",
                                type="article",
                            ),
                        ],
                    ),
                    RoadmapMilestone(
                        id="be-m2",
                        title="API Design with FastAPI & Pydantic",
                        description="Build clean REST endpoints, request validation, and status codes.",
                        estimated_hours=14,
                        skills_covered=["FastAPI", "Pydantic", "REST APIs"],
                        resources=[
                            RoadmapResource(
                                title="FastAPI Official Tutorial",
                                url="https://fastapi.tiangolo.com/tutorial/",
                                type="documentation",
                            ),
                        ],
                    ),
                ],
            ),
            RoadmapPhase(
                phase_number=2,
                title="Phase 2: Database Systems & Data Modeling",
                description="Relational database schemas, migrations, querying, and ORMs.",
                milestones=[
                    RoadmapMilestone(
                        id="be-m3",
                        title="Relational Schema Design & PostgreSQL",
                        description="Indexing, foreign keys, normalization, and ACID transactions.",
                        estimated_hours=16,
                        skills_covered=["PostgreSQL", "SQL", "Database Indexing"],
                        resources=[
                            RoadmapResource(
                                title="PostgreSQL Tutorial",
                                url="https://www.postgresqltutorial.com/",
                                type="course",
                            ),
                        ],
                    ),
                    RoadmapMilestone(
                        id="be-m4",
                        title="Supabase & ORM Integration (SQLAlchemy / Prisma)",
                        description="Connect backend services to cloud Postgres with real-time auth and storage.",
                        estimated_hours=12,
                        skills_covered=["Supabase", "ORM", "Cloud DB"],
                        resources=[
                            RoadmapResource(
                                title="Supabase Python Client Docs",
                                url="https://supabase.com/docs/reference/python",
                                type="documentation",
                            ),
                        ],
                    ),
                ],
            ),
            RoadmapPhase(
                phase_number=3,
                title="Phase 3: Production Engineering & Security",
                description="Testing, authentication, containerization, and API security.",
                milestones=[
                    RoadmapMilestone(
                        id="be-m5",
                        title="Authentication, JWT & Security Best Practices",
                        description="Password hashing, OAuth2 flows, RBAC, and rate limiting.",
                        estimated_hours=14,
                        skills_covered=["JWT", "Security", "OAuth2"],
                        resources=[
                            RoadmapResource(
                                title="FastAPI Security & OAuth2",
                                url="https://fastapi.tiangolo.com/tutorial/security/",
                                type="documentation",
                            ),
                        ],
                    ),
                    RoadmapMilestone(
                        id="be-m6",
                        title="Automated Testing & Docker Deployment",
                        description="Write pytest test suites, mock external services, and build Dockerfiles.",
                        estimated_hours=15,
                        skills_covered=["Pytest", "Docker", "CI/CD"],
                        resources=[
                            RoadmapResource(
                                title="Effective Python Testing with Pytest",
                                url="https://docs.pytest.org/",
                                type="documentation",
                            ),
                        ],
                    ),
                ],
            ),
        ]

    @staticmethod
    def _generate_frontend_phases(level: str) -> List[RoadmapPhase]:
        return [
            RoadmapPhase(
                phase_number=1,
                title="Phase 1: Modern JavaScript & CSS Architecture",
                description="Modern JavaScript ES6+, responsive design, and Tailwind CSS.",
                milestones=[
                    RoadmapMilestone(
                        id="fe-m1",
                        title="ES6+ JavaScript & DOM Concepts",
                        description="Promises, closures, fetch API, and browser event loop.",
                        estimated_hours=12,
                        skills_covered=["JavaScript", "ES6+", "Async JS"],
                    ),
                    RoadmapMilestone(
                        id="fe-m2",
                        title="Utility-First CSS with Tailwind",
                        description="Building responsive, accessible design systems.",
                        estimated_hours=10,
                        skills_covered=["Tailwind CSS", "Responsive Design"],
                    ),
                ],
            ),
            RoadmapPhase(
                phase_number=2,
                title="Phase 2: React Component Ecosystem",
                description="Hooks, state management, routing, and form handling.",
                milestones=[
                    RoadmapMilestone(
                        id="fe-m3",
                        title="React Hooks & State Architecture",
                        description="useState, useEffect, useMemo, custom hooks, and Context API.",
                        estimated_hours=16,
                        skills_covered=["React", "Custom Hooks", "Context API"],
                    ),
                    RoadmapMilestone(
                        id="fe-m4",
                        title="Single Page Routing & Backend Integration",
                        description="React Router v6, query params, Axios/Fetch, and error boundaries.",
                        estimated_hours=14,
                        skills_covered=["React Router", "API Integration"],
                    ),
                ],
            ),
        ]

    @staticmethod
    def _generate_data_phases(level: str) -> List[RoadmapPhase]:
        return [
            RoadmapPhase(
                phase_number=1,
                title="Phase 1: Data Manipulation & Statistical Foundations",
                description="NumPy, Pandas, exploratory data analysis, and visualization.",
                milestones=[
                    RoadmapMilestone(
                        id="ds-m1",
                        title="Data Wrangling with Pandas & NumPy",
                        description="Cleaning, transforming, grouping, and indexing large datasets.",
                        estimated_hours=15,
                        skills_covered=["Pandas", "NumPy", "EDA"],
                    ),
                ],
            ),
            RoadmapPhase(
                phase_number=2,
                title="Phase 2: Applied Machine Learning & Deployment",
                description="Supervised learning, model evaluation, and serving via FastAPI.",
                milestones=[
                    RoadmapMilestone(
                        id="ds-m2",
                        title="Scikit-Learn Modeling & Validation",
                        description="Regression, classification, cross-validation, and metrics.",
                        estimated_hours=18,
                        skills_covered=["Scikit-Learn", "Machine Learning"],
                    ),
                ],
            ),
        ]

