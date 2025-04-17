import pytest
from schemas import PostPayload, CommentPayload


@pytest.fixture
def new_post_payload(faker_fixture) -> dict:
    yield PostPayload(
        title=faker_fixture.sentence(nb_words=6),
        author=faker_fixture.name()
    ).model_dump()


@pytest.fixture
def new_comment_payload(faker_fixture) -> dict:
    yield CommentPayload(
        body=faker_fixture.sentence(nb_words=10),
        postId=''  # Default value
    ).model_dump()


@pytest.fixture
def create_valid_post(helper_posts, new_post_payload):
    yield helper_posts.create_post(payload=new_post_payload)
