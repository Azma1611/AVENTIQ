# AVENTIQ Architecture Overview

**Brand Tagline:** From Ambition to Achievement

## Vision
AVENTIQ is an AI-powered career development platform designed to empower college students, fresh graduates, job seekers, and career changers. It delivers:
- Personalized Career Roadmaps
- Skill Assessments & Gap Analysis
- Curated Learning Resources
- Interactive AI Mentorship

## System Components
1. **Frontend (`/frontend`):**
   - React + Vite SPA
   - Tailwind CSS for modern styling
   - React Router for client-side navigation
   - Modular folder structure: `components`, `pages`, `layouts`, `hooks`, `context`, `services`, `utils`, `styles`

2. **Backend (`/backend`):**
   - Python FastAPI application
   - Pydantic models for validation & schemas
   - Clean layer separation: `api`, `core`, `models`, `schemas`, `services`, `utils`
   - Future integration: Supabase (Auth + PostgreSQL)

