from typing import List

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from .news_fetcher import fetch_ai_news_general, fetch_ai_news_education
from .summarizer import summarize_articles
from .guardrails import filter_summaries
from .emailer import send_email
from .security import require_api_key, rate_limit, get_allowed_origins, is_email_domain_allowed


class ArticleSummary(BaseModel):
    id: str
    title: str
    link: str
    summary: str
    source: str
    category: str  # research|policy|product|education


class SendEmailRequest(BaseModel):
    email: EmailStr
    articles: List[ArticleSummary]


app = FastAPI(title="Research Agent API", version="0.1.0")

# Enable CORS for local development (Streamlit usually runs on 8501)
allowed_origins_env = get_allowed_origins()
allowed_origins = [o.strip() for o in allowed_origins_env.split(",")] if allowed_origins_env else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/ai-news", response_model=List[ArticleSummary], dependencies=[Depends(require_api_key), Depends(rate_limit)])
def get_ai_news() -> List[ArticleSummary]:
    raw_articles = fetch_ai_news_general()
    summarized = summarize_articles(raw_articles)
    moderated = filter_summaries(summarized)
    return moderated


@app.get("/ai-education", response_model=List[ArticleSummary], dependencies=[Depends(require_api_key), Depends(rate_limit)])
def get_ai_education_news() -> List[ArticleSummary]:
    raw_articles = fetch_ai_news_education()
    summarized = summarize_articles(raw_articles)
    moderated = filter_summaries(summarized)
    return moderated


@app.post("/send-email", dependencies=[Depends(require_api_key), Depends(rate_limit)])
def post_send_email(payload: SendEmailRequest) -> dict:
    if not is_email_domain_allowed(payload.email):
        raise HTTPException(status_code=403, detail="Email domain not allowed")
    try:
        send_email(payload.email, payload.articles)
        return {"success": True, "message": f"Email sent to {payload.email}"}
    except Exception as exc:  # pragma: no cover - simple mocked handler
        raise HTTPException(status_code=500, detail=str(exc))


