import os
import uuid
from enum import Enum

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
POSTS_ENDPOINT = "/posts"
COMMENTS_ENDPOINT = "/comments"
PROFILE_ENDPOINT = "/profile"
ROOT_WORKING_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_FOLDER = 'output'
NONEXISTENT_ID = uuid.uuid4()
EXTRA_FIELD = "extra_field"


class HTTPStatusCodes(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    TOO_MANY_REUQESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class PostFields(Enum):
    ID = "id"
    TITLE = "title"
    AUTHOR = "author"


class CommentFields(Enum):
    ID = "id"
    BODY = "body"
    POST_ID = "postId"


class BlogApiEndpointKeys(str, Enum):
    GET_POSTS = "GET_POSTS"
    GET_POST_BY_ID = "GET_POST_BY_ID"
    CREATE_POST = "CREATE_POST"
    UPDATE_POST = "UPDATE_POST"
    DELETE_POST = "DELETE_POST"

    GET_COMMENTS = "GET_COMMENTS"
    GET_COMMENT_BY_ID = "GET_COMMENT_BY_ID"
    CREATE_COMMENT = "CREATE_COMMENT"
    UPDATE_COMMENT = "UPDATE_COMMENT"
    DELETE_COMMENT = "DELETE_COMMENT"

    GET_PROFILE = "GET_PROFILE"
    UPDATE_PROFILE = "UPDATE_PROFILE"
