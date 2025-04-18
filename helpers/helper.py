import pytest
from request_builders.request_builder_blog import BlogApiController


class Helper:
    """
    Base helper class that provides generic API request functionality
    used by other specific helper classes (Posts, Comments, Profile, Performance).
    """
    def __init__(self):
        self.controller = BlogApiController()

    def _send_request(self, endpoint_key, expected_status, **kwargs):
        pytest.logger.info(f"Sending request: {endpoint_key}")
        response = self.controller.request(endpoint_key, **kwargs)
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}. Actual status code: {response.status_code}"

        expect_json = kwargs.get("expect_json", True)
        if expect_json:
            try:
                return response.json()
            except ValueError:
                return {}
        return None

    def _send_request_and_return_response(self, endpoint_key, **kwargs):
        pytest.logger.info(f"Sending request: {endpoint_key}")
        response = self.controller.request(endpoint_key, **kwargs)
        return response
