## Research Agent

Curated AI news with summaries. Two strands: General AI and AI in Education.

### Features
- FastAPI backend with endpoints: `/ai-news`, `/ai-education`, `/send-email`
- Streamlit frontend with card UI and email digest
- Mocked news fetcher, placeholder summarizer, simple guardrails, mock emailer

### Local Development
1. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
2. Run backend:
   ```bash
   uvicorn src.backend.main:app --reload
   ```
3. Run frontend:
   ```bash
   streamlit run src/frontend/app.py
   ```
4. (Optional) Configure API base URL in Streamlit secrets via `.streamlit/secrets.toml`:
   ```toml
   API_BASE_URL = "http://localhost:8000"
   ```

### Docker
Run both services:
```bash
docker compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:8501

### File Structure
```
src/
  backend/
    main.py
    news_fetcher.py
    summarizer.py
    emailer.py
    guardrails.py
  frontend/
    app.py
```

### Notes
- `news_fetcher.py`: replace with real news source and last-6-months filtering.
- `summarizer.py`: wire to an LLM for 2–4 sentence summaries.
- `emailer.py`: integrate a provider (e.g., SendGrid).
- `guardrails.py`: expand keyword list or add a moderation API.


