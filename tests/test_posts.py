import pytest
from schemas import PostModel


@pytest.mark.smoke
@pytest.mark.posts
@pytest.mark.regression
def test_get_all_posts(helper_posts):
    """Verify that GET /posts returns a list of posts."""
    posts_list = helper_posts.get_posts()
    pytest.logger.info(f"Returned {len(posts_list)} posts")
    assert isinstance(posts_list, list), "Expected response to be a list of posts"
    assert all("id" in post for post in posts_list), "Some posts are missing 'id' field"


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
    assert create_post_response["title"] == new_post_payload["title"]
    assert create_post_response["author"] == new_post_payload["author"]
    assert "id" in create_post_response

    get_created_post = helper_posts.get_post_by_id(post_id=create_post_response["id"])
    assert get_created_post["title"] == new_post_payload["title"]
    assert get_created_post["author"] == new_post_payload["author"]


@pytest.mark.posts
@pytest.mark.regression
def test_update_post(helper_posts, new_post_payload, faker_fixture):
    """Ensure that a post can be updated via PUT /posts/{id}."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)

    updated_payload = {
        "title": faker_fixture.sentence(nb_words=5),
        "author": faker_fixture.name()
    }

    updated_post = helper_posts.update_post(post_id=create_post_response["id"], payload=updated_payload)
    assert updated_post["title"] == updated_payload["title"]
    assert updated_post["author"] == updated_payload["author"]


@pytest.mark.posts
@pytest.mark.regression
def test_delete_post(helper_posts, new_post_payload):
    """Ensure a post can be deleted via DELETE /posts/{id}."""
    create_post_response = helper_posts.create_post(payload=new_post_payload)
    delete_post_response = helper_posts.delete_post(post_id=create_post_response["id"])
    assert create_post_response["title"] == delete_post_response["title"]
    assert create_post_response["author"] == delete_post_response["author"]
    helper_posts.get_post_by_id(post_id=create_post_response["id"], expected_status=404)


@pytest.mark.posts
@pytest.mark.negative
@pytest.mark.xfail(reason="JSON Server does not enforce schema validation thus it's going to fail")
@pytest.mark.regression
def test_create_post_missing_title(helper_posts):
    """Creating a post without a title should fail (but JSON Server doesn't validate)."""
    invalid_payload = {"author": "No Title Author"}
    helper_posts.create_post(payload=invalid_payload, expected_status=400)
