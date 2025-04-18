from core import BlogApiEndpointKeys, HTTPStatusCodes
from .helper import Helper


class HelperComments(Helper):
    """
    Helper class for handling all operations related to /comments endpoints.
    Includes create, retrieve, update, and delete functionalities for comments.
    """
    def __init__(self):
        super().__init__()

    def get_comments(self, expected_status=HTTPStatusCodes.OK.value):
        return self._send_request(BlogApiEndpointKeys.GET_COMMENTS, expected_status)

    def get_comment_by_id(self, comment_id: int, expected_status=HTTPStatusCodes.OK.value, expect_json=True):
        return self._send_request(BlogApiEndpointKeys.GET_COMMENT_BY_ID, expected_status, id=comment_id,
                                  expect_json=expect_json)

    def create_comment(self, payload: dict, expected_status=HTTPStatusCodes.CREATED.value):
        return self._send_request(BlogApiEndpointKeys.CREATE_COMMENT, expected_status, payload=payload)

    def update_comment(self, comment_id: int, payload: dict, expected_status=HTTPStatusCodes.OK.value):
        return self._send_request(BlogApiEndpointKeys.UPDATE_COMMENT, expected_status, payload=payload, id=comment_id)

    def delete_comment(self, comment_id: int, expected_status=HTTPStatusCodes.OK.value, expect_json=True):
        return self._send_request(BlogApiEndpointKeys.DELETE_COMMENT, expected_status, id=comment_id,
                                  expect_json=expect_json)
