from aiolimiter import AsyncLimiter
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import httpx
import logging

logger = logging.getLogger(__name__)

# Groq is fast but rate limited on free tier (usually ~30 req/min depending on model)
groq_limiter = AsyncLimiter(2, 1)

# Pexels (approx 200 requests / hour on free tier)
pexels_limiter = AsyncLimiter(2, 1)

# Pixabay (100 requests / min)
pixabay_limiter = AsyncLimiter(2, 1)

# Unsplash (50 requests / hour) -> be very careful here
unsplash_limiter = AsyncLimiter(1, 1)

# Giphy
giphy_limiter = AsyncLimiter(4, 1)

# Iconfinder
iconfinder_limiter = AsyncLimiter(2, 1)

def log_retry(retry_state):
    logger.warning(f"Retrying after error (Attempt {retry_state.attempt_number})...")

# Common retry decorator for httpx or groq exceptions
def with_retry():
    return retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        before_sleep=log_retry,
        reraise=True
    )
