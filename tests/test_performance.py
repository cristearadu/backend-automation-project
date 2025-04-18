import pytest
from core import HTTPStatusCodes
import threading


@pytest.mark.performance
@pytest.mark.posts
@pytest.mark.flaky_regression
@pytest.mark.xfail(reason="Rate limiting is not implemented on the server")
def test_rate_limiting_on_get_posts(helper_performance):
    """Send multiple rapid GET requests to /posts to check for rate limiting."""
    successes, failures, others = helper_performance.simulate_get_post_load()
    pytest.logger.info(
        f"[Threaded Rate Limit] {successes} successful | {failures} failed ({HTTPStatusCodes.TOO_MANY_REQUESTS.value}s)"
        f" | {others} other"
    )
    if failures == 0:
        pytest.logger.warning("Rate limiting does not seem to be implemented on GET /posts")

    assert failures >= 1, (
            f"Expected at least one {HTTPStatusCodes.TOO_MANY_REQUESTS.value} error under load"
        )
