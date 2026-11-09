from typing import List, Optional
from app.schemas.resource import ResourceItem, ResourceListResponse

_CATALOG: List[ResourceItem] = [
    ResourceItem(
        id="res-1",
        title="FastAPI Official Documentation & Interactive Tutorial",
        description="Comprehensive guide covering dependency injection, async routes, Pydantic models, and OpenAPI.",
        url="https://fastapi.tiangolo.com/",
        provider="FastAPI",
        type="documentation",
        skill_tags=["FastAPI", "Python", "REST", "AsyncIO"],
        difficulty="all_levels",
        estimated_hours=8,
        is_free=True,
    ),
    ResourceItem(
        id="res-2",
        title="PostgreSQL Tutorial for Developers",
        description="Step-by-step SQL tutorials covering table design, indexing, foreign keys, and query optimization.",
        url="https://www.postgresqltutorial.com/",
        provider="PostgreSQL Tutorial",
        type="course",
        skill_tags=["PostgreSQL", "SQL", "Databases"],
        difficulty="beginner",
        estimated_hours=12,
        is_free=True,
    ),
    ResourceItem(
        id="res-3",
        title="Full Stack Python: Web APIs & Architecture",
        description="Explains architectural patterns, WSGI/ASGI gateways, database connections, and security.",
        url="https://www.fullstackpython.com/application-programming-interfaces.html",
        provider="Full Stack Python",
        type="article",
        skill_tags=["Python", "Architecture", "REST"],
        difficulty="intermediate",
        estimated_hours=6,
        is_free=True,
    ),
    ResourceItem(
        id="res-4",
        title="Docker for Developers - Hands-on Crash Course",
        description="Learn containerization, Dockerfiles, docker-compose, and multi-stage production builds.",
        url="https://docker-curriculum.com/",
        provider="Docker Curriculum",
        type="course",
        skill_tags=["Docker", "DevOps", "Deployment"],
        difficulty="intermediate",
        estimated_hours=10,
        is_free=True,
    ),
    ResourceItem(
        id="res-5",
        title="System Design Primer by Donne Martin",
        description="Learn how to design large-scale systems and prepare for software engineering system design interviews.",
        url="https://github.com/donnemartin/system-design-primer",
        provider="GitHub Open Source",
        type="documentation",
        skill_tags=["System Design", "Scalability", "Architecture"],
        difficulty="advanced",
        estimated_hours=25,
        is_free=True,
    ),
]


class ResourceService:
    @staticmethod
    def list_resources(
        skill: Optional[str] = None,
        resource_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        search: Optional[str] = None,
    ) -> ResourceListResponse:
        filtered = _CATALOG

        if skill:
            skill_lower = skill.lower()
            filtered = [
                item for item in filtered
                if any(skill_lower in tag.lower() for tag in item.skill_tags)
            ]

        if resource_type:
            filtered = [item for item in filtered if item.type.lower() == resource_type.lower()]

        if difficulty and difficulty != "all_levels":
            filtered = [
                item for item in filtered
                if item.difficulty.lower() in (difficulty.lower(), "all_levels")
            ]

        if search:
            s = search.lower()
            filtered = [
                item for item in filtered
                if s in item.title.lower() or s in item.description.lower()
            ]

        return ResourceListResponse(
            total=len(filtered),
            items=filtered,
        )

