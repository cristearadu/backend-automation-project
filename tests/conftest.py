import pytest
from schemas.post import PostPayload


@pytest.fixture
def new_post_payload(faker_fixture):
    return PostPayload(
        title=faker_fixture.sentence(nb_words=6),
        author=faker_fixture.name()
    ).model_dump()  # returns as dict for usage in requests
