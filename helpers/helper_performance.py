import pytest
from .helper import Helper
from core import HTTPStatusCodes, BlogApiEndpointKeys
from concurrent.futures import ThreadPoolExecutor, as_completed


class HelperPerformance(Helper):
    """
    Helper class designed for performance and concurrency tests.
    Allows sending multiple parallel requests to simulate load or rate-limiting checks.
    """
    def __init__(self, threads=50):
        super().__init__()
        self.threads = threads

    def simulate_parallel_requests(
            self,
            request_fn,
            expected_success,
            expected_failure
    ):
        """
        Executes the provided request function in parallel across multiple threads.

        Args:
            request_fn (Callable): The function to call in each thread. Must return a status code.
            expected_success (int): Expected HTTP status code for a successful request.
            expected_failure (int): Expected HTTP status code for a failed (rate-limited) request.

        Returns:
            Tuple[int, int, int]: A count of (successes, failures, unexpected responses).
        """
        successes, failures, others = 0, 0, 0

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(request_fn) for _ in range(self.threads)]

            for future in as_completed(futures):
                try:
                    status_code = future.result()
                    if status_code == expected_failure:
                        failures += 1
                    elif status_code == expected_success:
                        successes += 1
                    else:
                        pytest.logger.warning(f"Unexpected response: {status_code}")
                        others += 1
                except Exception as e:
                    pytest.logger.error(f"Thread call error: {e}")
                    others += 1

        return successes, failures, others

    def simulate_get_post_load(self, expected_success=HTTPStatusCodes.OK.value,
                               expected_failure=HTTPStatusCodes.TOO_MANY_REQUESTS.value):
        """
        Simulates a high-load scenario by sending multiple concurrent GET /posts requests.

        Args:
            expected_success (int): Status code to treat as a success.
            expected_failure (int): Status code to treat as a rate-limit failure.

        Returns:
            Tuple[int, int, int]: A count of successes, failures, and unexpected results.
        """
        def make_call():
            response = self._send_request_and_return_response(BlogApiEndpointKeys.GET_POSTS)
            return response.status_code

        return self.simulate_parallel_requests(
            request_fn=make_call,
            expected_success=expected_success,
            expected_failure=expected_failure
        )
