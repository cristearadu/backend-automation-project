from request_builders.request_builder_blog import BlogApiController
from core import HTTPStatusCodes, BlogApiEndpointKeys


class HelperPosts:
    def __init__(self):
        self.controller = BlogApiController()

    def get_posts(self, expected_status=HTTPStatusCodes.OK.value) -> list:
        response = self.controller.request(BlogApiEndpointKeys.GET_POSTS)
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}. Actual status code: {response.status_code}"
        return response.json()

    def get_post_by_id(self, post_id, expected_status=HTTPStatusCodes.OK.value):
        response = self.controller.request(BlogApiEndpointKeys.GET_POST_BY_ID, id=post_id)
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}. Actual status code: {response.status_code}"
        return response.json() if response.status_code == HTTPStatusCodes.OK.value else {}

    def create_post(self, payload, expected_status=HTTPStatusCodes.CREATED.value):
        response = self.controller.request(BlogApiEndpointKeys.CREATE_POST, payload=payload)
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}. Actual status code: {response.status_code}"
        return response.json()

    def update_post(self, post_id, payload, expected_status=HTTPStatusCodes.OK.value):
        response = self.controller.request(BlogApiEndpointKeys.UPDATE_POST, id=post_id, payload=payload)
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}. Actual status code: {response.status_code}"
        return response.json()

    def delete_post(self, post_id, expected_status=HTTPStatusCodes.OK.value):
        response = self.controller.request(BlogApiEndpointKeys.DELETE_POST, id=post_id)
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}. Actual status code: {response.status_code}"
        return response.json()
