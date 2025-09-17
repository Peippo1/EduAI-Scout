import json
from typing import List, Dict

import requests
import streamlit as st


API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")


def fetch_news(endpoint: str) -> List[Dict]:
    resp = requests.get(f"{API_BASE_URL}{endpoint}")
    resp.raise_for_status()
    return resp.json()


def send_email(email: str, articles: List[Dict]) -> Dict:
    payload = {"email": email, "articles": articles}
    resp = requests.post(f"{API_BASE_URL}/send-email", json=payload)
    resp.raise_for_status()
    return resp.json()


def render_card(article: Dict, key: str) -> bool:
    with st.container(border=True):
        st.markdown(f"### {article['title']}")
        st.write(f"Source: {article.get('source', 'Unknown')} | Category: {article.get('category', '-')}")
        st.write(article.get("summary", ""))
        st.link_button("Open link", article.get("link", "#"))
        return st.checkbox("Select", key=key)


def main() -> None:
    st.set_page_config(page_title="Research Agent", layout="wide")
    st.title("Research Agent")
    st.caption("Curated AI news with quick summaries. Pick and email yourself a digest.")

    # Sidebar selection
    section = st.sidebar.radio("Strand", ["General AI", "AI in Education"], index=0)
    endpoint = "/ai-news" if section == "General AI" else "/ai-education"

    # Fetch data
    try:
        articles = fetch_news(endpoint)
    except Exception as exc:
        st.error(f"Failed to load articles: {exc}")
        return

    # Cards with selection
    st.subheader(section)
    selected: List[Dict] = []
    for article in articles:
        is_selected = render_card(article, key=f"select-{article['id']}")
        if is_selected:
            selected.append(article)

    # Footer: email sending
    st.divider()
    st.write("Send selected to email")
    email = st.text_input("Email address", placeholder="you@example.com")
    send_disabled = not (email and selected)
    if st.button("Send digest", disabled=send_disabled):
        try:
            resp = send_email(email, selected)
            st.success(resp.get("message", "Email sent."))
        except Exception as exc:
            st.error(f"Failed to send email: {exc}")


if __name__ == "__main__":
    main()


