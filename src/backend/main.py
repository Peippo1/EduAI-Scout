from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from .news_fetcher import fetch_ai_news_general, fetch_ai_news_education
from .summarizer import summarize_articles
from .guardrails import filter_summaries
from .emailer import send_email


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/ai-news", response_model=List[ArticleSummary])
def get_ai_news() -> List[ArticleSummary]:
    raw_articles = fetch_ai_news_general()
    summarized = summarize_articles(raw_articles)
    moderated = filter_summaries(summarized)
    return moderated


@app.get("/ai-education", response_model=List[ArticleSummary])
def get_ai_education_news() -> List[ArticleSummary]:
    raw_articles = fetch_ai_news_education()
    summarized = summarize_articles(raw_articles)
    moderated = filter_summaries(summarized)
    return moderated


@app.post("/send-email")
def post_send_email(payload: SendEmailRequest) -> dict:
    try:
        send_email(payload.email, payload.articles)
        return {"success": True, "message": f"Email sent to {payload.email}"}
    except Exception as exc:  # pragma: no cover - simple mocked handler
        raise HTTPException(status_code=500, detail=str(exc))


