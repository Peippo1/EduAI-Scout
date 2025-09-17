from typing import List, Dict


def send_email(email_address: str, articles: List[Dict]) -> None:
    # Placeholder emailer. Replace with real provider (e.g., SendGrid) later.
    print(f"Email sent to {email_address} with {len(articles)} articles.")


