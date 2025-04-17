from enum import Enum
from core import BASE_URL, http_request, BlogApiEndpointKeys


class BlogApiEndpoints(Enum):
    GET_POSTS = ("GET", f"{BASE_URL}/posts", BlogApiEndpointKeys.GET_POSTS)
    GET_POST_BY_ID = ("GET", f"{BASE_URL}/posts/{{id}}", BlogApiEndpointKeys.GET_POST_BY_ID)
    CREATE_POST = ("POST", f"{BASE_URL}/posts", BlogApiEndpointKeys.CREATE_POST)
    UPDATE_POST = ("PUT", f"{BASE_URL}/posts/{{id}}", BlogApiEndpointKeys.UPDATE_POST)
    DELETE_POST = ("DELETE", f"{BASE_URL}/posts/{{id}}", BlogApiEndpointKeys.DELETE_POST)

    GET_COMMENTS = ("GET", f"{BASE_URL}/comments", BlogApiEndpointKeys.GET_COMMENTS)
    GET_COMMENT_BY_ID = ("GET", f"{BASE_URL}/comments/{{id}}", BlogApiEndpointKeys.GET_COMMENT_BY_ID)
    CREATE_COMMENT = ("POST", f"{BASE_URL}/comments", BlogApiEndpointKeys.CREATE_COMMENT)
    UPDATE_COMMENT = ("PUT", f"{BASE_URL}/comments/{{id}}", BlogApiEndpointKeys.UPDATE_COMMENT)
    DELETE_COMMENT = ("DELETE", f"{BASE_URL}/comments/{{id}}", BlogApiEndpointKeys.DELETE_COMMENT)

    GET_PROFILE = ("GET", f"{BASE_URL}/profile", BlogApiEndpointKeys.GET_PROFILE)
    UPDATE_PROFILE = ("PUT", f"{BASE_URL}/profile", BlogApiEndpointKeys.UPDATE_PROFILE)

    def __init__(self, method, path, key):
        self.method = method
        self.path = path
        self.key = key


class BlogApiController:
    def request(self, key, headers=None, payload=None, **kwargs):
        endpoint = next((e for e in BlogApiEndpoints if e.key == key), None)
        if not endpoint:
            raise ValueError(f"Unknown endpoint key: {key}")

        formatted_url = endpoint.path.format(**kwargs)
        return http_request(endpoint.method, formatted_url, headers=headers, json=payload)
