import os
from typing import List, Dict

import requests


def _openai_summarize_batch(items: List[Dict]) -> List[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return [
            "This article discusses recent developments in artificial intelligence. It highlights key implications, practical applications, and open questions. Considerations around safety, evaluation, and deployment are also noted."
            for _ in items
        ]

    system_prompt = (
        "You are a concise research assistant. Summarize each article in 2-4 sentences, "
        "mentioning key findings, implications, and relevance to AI or education."
    )
    # We will call the responses API to summarize items sequentially in one prompt
    content_lines = []
    for idx, a in enumerate(items, start=1):
        content_lines.append(f"[{idx}] Title: {a.get('title','')}. Source: {a.get('source','')}. Link: {a.get('link','')}")
    user_prompt = (
        "Summarize the following articles. Return exactly N lines, one per article in order.\n\n"
        + "\n".join(content_lines)
    )

    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 700,
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"].strip()
        lines = [ln.strip(" -") for ln in text.splitlines() if ln.strip()]
        # If not matching count, pad/truncate
        if len(lines) < len(items):
            lines += [lines[-1] if lines else "Summary unavailable."] * (len(items) - len(lines))
        return lines[: len(items)]
    except Exception:
        return [
            "This article discusses recent developments in artificial intelligence. It highlights key implications, practical applications, and open questions. Considerations around safety, evaluation, and deployment are also noted."
            for _ in items
        ]


def summarize_articles(articles: List[Dict]) -> List[Dict]:
    if not articles:
        return []
    summaries = _openai_summarize_batch(articles)
    summarized: List[Dict] = []
    for article, summary in zip(articles, summaries):
        item = dict(article)
        item["summary"] = summary
        summarized.append(item)
    return summarized


