import os
from datetime import datetime, timedelta
from typing import List, Dict
import requests

from .cache import cache


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def fetch_ai_news_general() -> List[Dict]:
    # Cached
    cached = cache.get("ai_general")
    if cached is not None:
        return cached

    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        # Fallback mocked articles if key not set
        data = [
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
        cache.set("ai_general", data, ttl_seconds=6 * 60 * 60)
        return data

    # Use Perplexity for recent AI news (last 6 months)
    six_months_ago = (datetime.utcnow() - timedelta(days=180)).date().isoformat()
    query = f"AI news after:{six_months_ago} site:theverge.com OR site:techcrunch.com OR site:nature.com OR site:arxiv.org"
    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar-small-online",
                "messages": [
                    {"role": "system", "content": "Return recent AI news results as JSON array with fields: id, title, link, source, category."},
                    {"role": "user", "content": query},
                ],
                "max_tokens": 800,
                "temperature": 0.2,
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        # Expect content to be JSON; if not, fallback to empty list
        try:
            import json as _json

            articles = _json.loads(content)
        except Exception:
            articles = []
    except Exception:
        articles = []

    # Normalize and limit
    normalized: List[Dict] = []
    for idx, a in enumerate(articles[:12]):
        normalized.append(
            {
                "id": a.get("id") or f"gen-{idx+1}",
                "title": a.get("title", "Untitled"),
                "link": a.get("link", ""),
                "summary": "",
                "source": a.get("source", "Unknown"),
                "category": a.get("category", "research"),
                "published_at": a.get("published_at", _now_iso()),
            }
        )

    cache.set("ai_general", normalized, ttl_seconds=6 * 60 * 60)
    return normalized


def fetch_ai_news_education() -> List[Dict]:
    cached = cache.get("ai_education")
    if cached is not None:
        return cached

    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        data = [
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
        cache.set("ai_education", data, ttl_seconds=6 * 60 * 60)
        return data

    six_months_ago = (datetime.utcnow() - timedelta(days=180)).date().isoformat()
    query = f"AI in education news after:{six_months_ago} site:edsurge.com OR site:insidehighered.com OR site:chronicle.com OR site:arxiv.org"
    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar-small-online",
                "messages": [
                    {"role": "system", "content": "Return recent AI-in-education news results as JSON array with fields: id, title, link, source, category."},
                    {"role": "user", "content": query},
                ],
                "max_tokens": 800,
                "temperature": 0.2,
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        try:
            import json as _json

            articles = _json.loads(content)
        except Exception:
            articles = []
    except Exception:
        articles = []

    normalized: List[Dict] = []
    for idx, a in enumerate(articles[:12]):
        normalized.append(
            {
                "id": a.get("id") or f"edu-{idx+1}",
                "title": a.get("title", "Untitled"),
                "link": a.get("link", ""),
                "summary": "",
                "source": a.get("source", "Unknown"),
                "category": a.get("category", "education"),
                "published_at": a.get("published_at", _now_iso()),
            }
        )

    cache.set("ai_education", normalized, ttl_seconds=6 * 60 * 60)
    return normalized


