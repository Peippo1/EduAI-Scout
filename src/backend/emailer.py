import os
from typing import List, Dict

import requests


def _build_html(articles: List[Dict]) -> str:
    rows = []
    for a in articles:
        rows.append(
            f"<div style='margin-bottom:16px'><h3>{a.get('title','')}</h3><p><em>{a.get('source','')}</em> | {a.get('category','')}</p><p>{a.get('summary','')}</p><p><a href='{a.get('link','')}' target='_blank'>Read more</a></p></div>"
        )
    return "".join(rows) or "<p>No articles selected.</p>"


def send_email(email_address: str, articles: List[Dict]) -> None:
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        print(f"Email sent to {email_address} with {len(articles)} articles (mock).")
        return

    from_email = os.environ.get("MAIL_FROM_EMAIL", "no-reply@example.com")
    from_name = os.environ.get("MAIL_FROM_NAME", "EduAI Scout")

    html = _build_html(articles)
    payload = {
        "personalizations": [{"to": [{"email": email_address}]}],
        "from": {"email": from_email, "name": from_name},
        "subject": "Your AI news digest",
        "content": [{"type": "text/html", "value": html}],
    }

    resp = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=15,
    )
    if resp.status_code >= 300:
        raise RuntimeError(f"SendGrid error: {resp.status_code} {resp.text}")


