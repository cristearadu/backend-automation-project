from request_builders.request_builder_blog import BlogApiController
from core import HTTPStatusCodes, BlogApiEndpointKeys


class HelperPosts:
    def __init__(self):
        self.controller = BlogApiController()

    def _send_request(self, endpoint_key, expected_status, payload=None, id=None, expect_json=True):
        response = self.controller.request(endpoint_key, payload=payload, id=id)
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}. Actual status code: {response.status_code}"

        if expect_json:
            try:
                return response.json()
            except ValueError:
                return {}
        return None

    def get_posts(self, expected_status=HTTPStatusCodes.OK.value) -> list:
        return self._send_request(BlogApiEndpointKeys.GET_POSTS, expected_status)

    def get_post_by_id(self, post_id, expected_status=HTTPStatusCodes.OK.value, expect_json=True):
        return self._send_request(BlogApiEndpointKeys.GET_POST_BY_ID, expected_status, id=post_id, expect_json=expect_json)

    def create_post(self, payload, expected_status=HTTPStatusCodes.CREATED.value):
        return self._send_request(BlogApiEndpointKeys.CREATE_POST, expected_status, payload=payload)

    def update_post(self, post_id, payload, expected_status=HTTPStatusCodes.OK.value):
        return self._send_request(BlogApiEndpointKeys.UPDATE_POST, expected_status, payload=payload, id=post_id)

    def delete_post(self, post_id, expected_status=HTTPStatusCodes.OK.value, expect_json=True):
        return self._send_request(BlogApiEndpointKeys.DELETE_POST, expected_status, id=post_id, expect_json=expect_json)