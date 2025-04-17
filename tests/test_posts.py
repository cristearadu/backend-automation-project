import pytest
from schemas import PostModel
from core import NONEXISTENT_ID, EXTRA_FIELD, HTTPStatusCodes, PostFields


@pytest.mark.smoke
@pytest.mark.posts
@pytest.mark.regression
def test_get_all_posts(helper_posts):
    """Verify that GET /posts returns a list of posts."""
    posts_list = helper_posts.get_posts()
    pytest.logger.info(f"Returned {len(posts_list)} posts")
    assert isinstance(posts_list, list), "Expected response to be a list of posts"
    assert all(PostFields.ID.value in post for post in posts_list), "Some posts are missing 'id' field"


@pytest.mark.smoke
@pytest.mark.schema
@pytest.mark.posts
@pytest.mark.regression
def test_post_response_matches_schema(helper_posts, new_post_payload):
    """Ensure that a newly created post response conforms to the defined schema."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info("Validating post schema...")

    post_obj = PostModel(**create_post_response)


@pytest.mark.posts
@pytest.mark.regression
def test_create_post(helper_posts, new_post_payload):
    """Verify that a new post can be created via POST /posts."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)

    pytest.logger.info(f"Created post: {create_post_response}")
    assert create_post_response[PostFields.TITLE.value] == new_post_payload[PostFields.TITLE.value]
    assert create_post_response[PostFields.AUTHOR.value] == new_post_payload[PostFields.AUTHOR.value]
    assert PostFields.ID.value in create_post_response

    get_created_post = helper_posts.get_post_by_id(post_id=create_post_response[PostFields.ID.value])
    assert get_created_post[PostFields.TITLE.value] == new_post_payload[PostFields.TITLE.value]
    assert get_created_post[PostFields.AUTHOR.value] == new_post_payload[PostFields.AUTHOR.value]


@pytest.mark.posts
@pytest.mark.regression
def test_update_post(helper_posts, new_post_payload, faker_fixture):
    """Ensure that a post can be updated via PUT /posts/{id}."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)

    updated_payload = {
        PostFields.TITLE.value: faker_fixture.sentence(nb_words=5),
        PostFields.AUTHOR.value: faker_fixture.name()
    }

    updated_post = helper_posts.update_post(post_id=create_post_response[PostFields.ID.value], payload=updated_payload)
    assert updated_post[PostFields.TITLE.value] == updated_payload[PostFields.TITLE.value]
    assert updated_post[PostFields.AUTHOR.value] == updated_payload[PostFields.AUTHOR.value]


@pytest.mark.posts
@pytest.mark.regression
def test_delete_post(helper_posts, new_post_payload):
    """Ensure a post can be deleted via DELETE /posts/{id}."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)
    delete_post_response = helper_posts.delete_post(post_id=create_post_response[PostFields.ID.value])
    assert create_post_response[PostFields.TITLE.value] == delete_post_response[PostFields.TITLE.value]
    assert create_post_response[PostFields.AUTHOR.value] == delete_post_response[PostFields.AUTHOR.value]
    helper_posts.get_post_by_id(post_id=create_post_response[PostFields.ID.value], expected_status=HTTPStatusCodes.NOT_FOUND.value)


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.regression
def test_delete_nonexistent_post(helper_posts):
    """Deleting a non-existent post should return 404."""
    helper_posts.delete_post(post_id=NONEXISTENT_ID, expected_status=HTTPStatusCodes.NOT_FOUND.value)

@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.xfail(reason="JSON Server does not enforce schema validation thus it's going to fail")
@pytest.mark.regression
def test_create_post_missing_title(helper_posts):
    """Creating a post without a title should fail (but JSON Server doesn't validate)."""
    invalid_payload = {PostFields.AUTHOR.value: "No Title Author"}
    helper_posts.create_post(payload=invalid_payload, expected_status=HTTPStatusCodes.BAD_REQUEST.value)


@pytest.mark.posts
@pytest.mark.edgecase
@pytest.mark.regression
def test_update_post_with_empty_title(helper_posts, new_post_payload):
    """Updating a post with empty title should still succeed (if allowed)."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)

    updated_payload = {
        PostFields.TITLE.value: "",
        PostFields.AUTHOR.value: create_post_response[PostFields.AUTHOR.value]
    }

    updated = helper_posts.update_post(post_id=create_post_response[PostFields.ID.value], payload=updated_payload)
    assert updated[PostFields.TITLE.value] == ""


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.regression
def test_get_nonexistent_post_returns_404(helper_posts):
    """Fetching a non-existent post should return 404."""
    non_existent_id = NONEXISTENT_ID
    helper_posts.get_post_by_id(post_id=non_existent_id, expected_status=HTTPStatusCodes.NOT_FOUND.value)


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.regression
def test_delete_post_twice_returns_404(helper_posts, new_post_payload):
    """Ensure deleting the same post twice yields a 404 the second time."""
    created_post = helper_posts.create_post(payload=new_post_payload)
    helper_posts.delete_post(post_id=created_post[PostFields.ID.value])
    helper_posts.delete_post(post_id=created_post[PostFields.ID.value], expected_status=HTTPStatusCodes.NOT_FOUND.value)


@pytest.mark.posts
@pytest.mark.edgecase
@pytest.mark.xfail(reason="JSON Server does not enforce not creating extra fields. Should fail")
@pytest.mark.regression
def test_create_post_with_extra_fields(helper_posts, new_post_payload, faker_fixture):
    """Creating a post with extra fields should still succeed (if allowed)."""
    new_post_payload[EXTRA_FIELD]= faker_fixture.sentence(nb_words=6)
    response = helper_posts.create_post(payload=new_post_payload)
    assert EXTRA_FIELD not in response, f"Should ignore the extra field: {EXTRA_FIELD} in {response}"


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.regression
def test_update_nonexistent_post(helper_posts, new_post_payload):
    helper_posts.update_post(
        post_id=NONEXISTENT_ID,
        payload=new_post_payload,
        expected_status=HTTPStatusCodes.NOT_FOUND.value
    )


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.xfail(reason="JSON Server allows empty objects, real API should not")
def test_create_post_with_empty_payload(helper_posts):
    """Creating a post with an empty body should fail (if validation is enforced)."""
    empty_payload = {}
    helper_posts.create_post(payload=empty_payload, expected_status=400)
