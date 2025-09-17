from typing import List, Dict


DEFAULT_BANNED_KEYWORDS = {"nsfw", "explicit", "hate", "violence"}


def filter_summaries(articles: List[Dict], banned_keywords: set = DEFAULT_BANNED_KEYWORDS) -> List[Dict]:
    def is_clean(text: str) -> bool:
        lowered = text.lower()
        return not any(keyword in lowered for keyword in banned_keywords)

    filtered: List[Dict] = []
    for article in articles:
        title_ok = is_clean(article.get("title", ""))
        summary_ok = is_clean(article.get("summary", ""))
        if title_ok and summary_ok:
            filtered.append(article)
    return filtered


