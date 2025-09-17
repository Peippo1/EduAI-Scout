import os
import time
from collections import defaultdict, deque
from typing import Deque, Dict, Optional

from fastapi import Depends, Header, HTTPException, Request


# Simple in-memory rate limiter per API key (or IP if no key)
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.key_to_requests: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds
        dq = self.key_to_requests[key]
        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        dq.append(now)


def get_backend_api_key() -> Optional[str]:
    return os.environ.get("BACKEND_API_KEY")


def get_allowed_origins() -> Optional[str]:
    return os.environ.get("ALLOWED_ORIGINS")


def get_allowed_email_domains() -> Optional[str]:
    return os.environ.get("ALLOWED_EMAIL_DOMAINS")


def get_rate_limiter() -> RateLimiter:
    max_requests = int(os.environ.get("RATE_LIMIT_MAX", "60"))
    window_seconds = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", "60"))
    return RateLimiter(max_requests=max_requests, window_seconds=window_seconds)


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    expected = get_backend_api_key()
    if expected:
        # If an API key is configured, require it
        if not x_api_key or x_api_key != expected:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
    # If no API key configured, allow all (dev mode)


def rate_limit(request: Request, x_api_key: Optional[str] = Header(default=None)) -> None:
    limiter = get_rate_limiter()
    key = x_api_key or request.client.host
    limiter.check(key)


def is_email_domain_allowed(email: str) -> bool:
    allowed = get_allowed_email_domains()
    if not allowed:
        return True
    domains = {d.strip().lower() for d in allowed.split(",") if d.strip()}
    try:
        domain = email.split("@", 1)[1].lower()
    except Exception:
        return False
    return domain in domains


