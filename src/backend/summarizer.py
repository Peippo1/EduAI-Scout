from typing import List, Dict


PLACEHOLDER_SUMMARY = (
    "This article discusses recent developments in artificial intelligence. "
    "It highlights key implications, practical applications, and open questions. "
    "Considerations around safety, evaluation, and deployment are also noted."
)


def summarize_articles(articles: List[Dict]) -> List[Dict]:
    summarized: List[Dict] = []
    for article in articles:
        item = dict(article)
        # Use placeholder text for now; later replace with LLM summarization
        item["summary"] = PLACEHOLDER_SUMMARY
        summarized.append(item)
    return summarized


