from datetime import datetime
from typing import List, Dict


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def fetch_ai_news_general() -> List[Dict]:
    # Mocked articles; replace with real news API integration later
    return [
        {
            "id": "gen-1",
            "title": "Major LLM update improves reasoning benchmarks",
            "link": "https://example.com/llm-update",
            "summary": "",
            "source": "Example News",
            "category": "research",
            "published_at": _now_iso(),
        },
        {
            "id": "gen-2",
            "title": "New AI safety policy draft opens for public comment",
            "link": "https://example.com/ai-policy-draft",
            "summary": "",
            "source": "Policy Watch",
            "category": "policy",
            "published_at": _now_iso(),
        },
        {
            "id": "gen-3",
            "title": "Startup launches AI-powered productivity tool",
            "link": "https://example.com/ai-productivity",
            "summary": "",
            "source": "Tech Daily",
            "category": "product",
            "published_at": _now_iso(),
        },
    ]


def fetch_ai_news_education() -> List[Dict]:
    # Mocked education-focused articles
    return [
        {
            "id": "edu-1",
            "title": "Universities pilot AI tutors in intro courses",
            "link": "https://example.com/ai-tutors",
            "summary": "",
            "source": "Campus Chronicle",
            "category": "education",
            "published_at": _now_iso(),
        },
        {
            "id": "edu-2",
            "title": "Study shows mixed outcomes for AI grading tools",
            "link": "https://example.com/ai-grading-study",
            "summary": "",
            "source": "Ed Research",
            "category": "education",
            "published_at": _now_iso(),
        },
    ]


