from core import HTTPStatusCodes, BlogApiEndpointKeys
from .helper import Helper


class HelperPosts(Helper):
    """
    Helper class for handling all operations related to /posts endpoints.
    Includes create, retrieve, update, and delete functionalities.
    """
    def __init__(self):
        super().__init__()

    def get_posts(self, expected_status=HTTPStatusCodes.OK.value) -> list:
        return self._send_request(BlogApiEndpointKeys.GET_POSTS, expected_status)

    def get_post_by_id(self, post_id, expected_status=HTTPStatusCodes.OK.value, expect_json=True):
        return self._send_request(BlogApiEndpointKeys.GET_POST_BY_ID, expected_status, id=post_id,
                                  expect_json=expect_json)

    def create_post(self, payload, expected_status=HTTPStatusCodes.CREATED.value):
        return self._send_request(BlogApiEndpointKeys.CREATE_POST, expected_status, payload=payload)

    def update_post(self, post_id, payload, expected_status=HTTPStatusCodes.OK.value):
        return self._send_request(BlogApiEndpointKeys.UPDATE_POST, expected_status, payload=payload, id=post_id)

    def delete_post(self, post_id, expected_status=HTTPStatusCodes.OK.value, expect_json=True):
        return self._send_request(BlogApiEndpointKeys.DELETE_POST, expected_status, id=post_id, expect_json=expect_json)
