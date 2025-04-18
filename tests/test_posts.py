import pytest
from schemas import PostModel
from core import NONEXISTENT_ID, HTTPStatusCodes, PostFields
from pydantic_core._pydantic_core import ValidationError
from test_data import NEGATIVE_POST_PAYLOADS


@pytest.mark.smoke
@pytest.mark.posts
@pytest.mark.flaky_regression
def test_get_all_posts(helper_posts):
    """Verify that GET /posts returns a list of posts."""
    posts_list = helper_posts.get_posts()
    pytest.logger.info(f"Returned {len(posts_list)} posts from GET /posts")
    assert isinstance(posts_list, list), "Expected response to be a list of posts"
    assert all(PostFields.ID.value in post for post in posts_list), "Some posts are missing 'id' field"


@pytest.mark.smoke
@pytest.mark.schema
@pytest.mark.posts
@pytest.mark.flaky_regression
def test_post_response_matches_schema(helper_posts, new_post_payload):
    """Ensure that a newly created post response conforms to the defined schema."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info(f"Created post for schema validation: {create_post_response}")
    try:
        PostModel(**create_post_response)
    except ValidationError as e:
        pytest.logger.error(f"PostModel response schema has failed: {e}")
        pytest.fail(f"Schema validation failed for PostModel: {e}")


@pytest.mark.posts
@pytest.mark.flaky_regression
def test_create_post(helper_posts, new_post_payload):
    """Verify that a new post can be created via POST /posts."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info(f"Created post: {create_post_response}")

    assert create_post_response[PostFields.TITLE.value] == new_post_payload[PostFields.TITLE.value]
    assert create_post_response[PostFields.AUTHOR.value] == new_post_payload[PostFields.AUTHOR.value]
    assert PostFields.ID.value in create_post_response

    get_created_post = helper_posts.get_post_by_id(post_id=create_post_response[PostFields.ID.value])
    pytest.logger.info(f"Verified post fetched after creation: {get_created_post}")

    assert get_created_post[PostFields.TITLE.value] == new_post_payload[PostFields.TITLE.value]
    assert get_created_post[PostFields.AUTHOR.value] == new_post_payload[PostFields.AUTHOR.value]


@pytest.mark.posts
@pytest.mark.flaky_regression
def test_update_post(helper_posts, new_post_payload, faker_fixture):
    """Ensure that a post can be updated via PUT /posts/{id}."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info(f"Created post to update: {create_post_response}")

    updated_payload = {
        PostFields.TITLE.value: faker_fixture.sentence(nb_words=5),
        PostFields.AUTHOR.value: faker_fixture.name()
    }

    updated_post = helper_posts.update_post(post_id=create_post_response[PostFields.ID.value], payload=updated_payload)
    pytest.logger.info(f"Updated post: {updated_post}")

    assert updated_post[PostFields.TITLE.value] == updated_payload[PostFields.TITLE.value]
    assert updated_post[PostFields.AUTHOR.value] == updated_payload[PostFields.AUTHOR.value]


@pytest.mark.posts
@pytest.mark.flaky_regression
def test_delete_post(helper_posts, new_post_payload):
    """Ensure a post can be deleted via DELETE /posts/{id}."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info(f"Created post to delete: {create_post_response}")

    delete_post_response = helper_posts.delete_post(post_id=create_post_response[PostFields.ID.value])
    pytest.logger.info(f"Deleted post: {delete_post_response}")

    assert create_post_response[PostFields.TITLE.value] == delete_post_response[PostFields.TITLE.value]
    assert create_post_response[PostFields.AUTHOR.value] == delete_post_response[PostFields.AUTHOR.value]

    helper_posts.get_post_by_id(post_id=create_post_response[PostFields.ID.value],
                                expected_status=HTTPStatusCodes.NOT_FOUND.value)
    pytest.logger.info(f"Verified post with ID {create_post_response[PostFields.ID.value]} is deleted")


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.flaky_regression
def test_delete_nonexistent_post(helper_posts):
    """Deleting a non-existent post should return 404."""
    pytest.logger.info(f"Trying to delete non-existent post ID {NONEXISTENT_ID}")
    helper_posts.delete_post(post_id=NONEXISTENT_ID, expected_status=HTTPStatusCodes.NOT_FOUND.value)


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.flaky_regression
def test_get_nonexistent_post_returns_404(helper_posts):
    """Fetching a non-existent post should return 404."""
    pytest.logger.info(f"Fetching non-existent post ID {NONEXISTENT_ID}")
    helper_posts.get_post_by_id(post_id=NONEXISTENT_ID, expected_status=HTTPStatusCodes.NOT_FOUND.value)


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.flaky_regression
def test_delete_post_twice_returns_404(helper_posts, new_post_payload):
    """Ensure deleting the same post twice yields a 404 the second time."""
    created_post = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info(f"Created post for delete-twice test: {created_post}")

    helper_posts.delete_post(post_id=created_post[PostFields.ID.value])
    pytest.logger.info("First delete successful")

    helper_posts.delete_post(post_id=created_post[PostFields.ID.value], expected_status=HTTPStatusCodes.NOT_FOUND.value)
    pytest.logger.info("Second delete returned 404 as expected")


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.flaky_regression
@pytest.mark.parametrize(
    "payload, is_update, expected_status, test_title", NEGATIVE_POST_PAYLOADS
)
def test_post_payload_negative_cases(helper_posts, new_post_payload, create_valid_post, payload, is_update,
                                     expected_status, test_title):
    """Test various invalid payloads for create and update post operations."""
    pytest.logger.info(f"Running test {test_title}")
    if is_update:
        pytest.logger.info(f"Trying to update post ID {create_valid_post[PostFields.ID.value]} with payload: {payload}")
        helper_posts.update_post(
            post_id=create_valid_post[PostFields.ID.value],
            payload=payload,
            expected_status=expected_status)
    else:
        pytest.logger.info(f"Trying to create post with payload: {payload}")
        helper_posts.create_post(payload=payload, expected_status=expected_status)
