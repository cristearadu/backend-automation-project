import pytest
from schemas import CommentModel
from core import HTTPStatusCodes, CommentFields, PostFields, NONEXISTENT_ID
from pydantic_core._pydantic_core import ValidationError
from test_data import NEGATIVE_COMMENT_PAYLOADS


@pytest.mark.smoke
@pytest.mark.comments
@pytest.mark.flaky_regression
def test_get_all_comments(helper_comments):
    """Verify that GET /comments returns a list of comments."""
    comments_list = helper_comments.get_comments()
    pytest.logger.info(f"Returned {len(comments_list)} comments")
    assert isinstance(comments_list, list), "Expected response to be a list of comments"
    assert all(CommentFields.ID.value in comment for comment in comments_list), "Some comments are missing 'id' field"


@pytest.mark.schema
@pytest.mark.comments
@pytest.mark.flaky_regression
def test_comment_response_matches_schema(helper_comments, new_comment_payload, create_valid_post):
    """Ensure that a newly created comment response matches the schema."""
    new_comment_payload[CommentFields.POST_ID.value] = create_valid_post[PostFields.ID.value]
    created_comment = helper_comments.create_comment(payload=new_comment_payload)
    pytest.logger.info("Validating comment schema...")
    try:
        CommentModel(**created_comment)
    except ValidationError as e:
        pytest.logger.error(f"CommentModel response schema has failed: {e}")
        pytest.fail(f"Schema validation failed for CommentModel: {e}")


@pytest.mark.comments
@pytest.mark.flaky_regression
def test_get_comment_by_id_successfully(helper_comments, new_comment_payload, create_valid_post):
    """Ensure a comment can be retrieved by ID."""
    new_comment_payload[CommentFields.POST_ID.value] = create_valid_post[PostFields.ID.value]
    created_comment = helper_comments.create_comment(payload=new_comment_payload)

    fetched_comment = helper_comments.get_comment_by_id(comment_id=created_comment[CommentFields.ID.value])
    assert fetched_comment[CommentFields.ID.value] == created_comment[CommentFields.ID.value]


@pytest.mark.comments
@pytest.mark.negative
@pytest.mark.flaky_regression
def test_get_nonexistent_comment_returns_404(helper_comments):
    """Ensure that fetching a nonexistent comment returns 404."""
    helper_comments.get_comment_by_id(comment_id=NONEXISTENT_ID, expected_status=HTTPStatusCodes.NOT_FOUND.value, expect_json=False)


@pytest.mark.comments
@pytest.mark.flaky_regression
def test_create_comment(helper_comments, new_comment_payload, create_valid_post):
    """Verify that a new comment can be created."""
    new_comment_payload[CommentFields.POST_ID.value] = create_valid_post[PostFields.ID.value]
    created_comment = helper_comments.create_comment(payload=new_comment_payload)
    pytest.logger.info(f"Created comment: {created_comment}")
    assert created_comment[CommentFields.BODY.value] == new_comment_payload[CommentFields.BODY.value]
    assert created_comment[CommentFields.POST_ID.value] == new_comment_payload[CommentFields.POST_ID.value]
    assert CommentFields.ID.value in created_comment


@pytest.mark.comments
@pytest.mark.flaky_regression
def test_update_comment_body(helper_comments, create_valid_post, new_comment_payload, faker_fixture):
    """Ensure that a comment body can be updated."""
    new_comment_payload[CommentFields.POST_ID.value] = create_valid_post[PostFields.ID.value]
    created_comment = helper_comments.create_comment(payload=new_comment_payload)

    updated_payload = {
        CommentFields.BODY.value: faker_fixture.sentence(nb_words=8),
        CommentFields.POST_ID.value: create_valid_post[PostFields.ID.value]
    }

    updated_comment = helper_comments.update_comment(
        comment_id=created_comment[CommentFields.ID.value],
        payload=updated_payload
    )
    pytest.logger.info(f"Updated comment {created_comment[CommentFields.ID.value]} body: {updated_comment}")
    assert updated_comment[CommentFields.BODY.value] == updated_payload[CommentFields.BODY.value]
    assert updated_comment[CommentFields.POST_ID.value] == created_comment[CommentFields.POST_ID.value]


@pytest.mark.comments
@pytest.mark.flaky_regression
@pytest.mark.xfail(reason="POST ID of a comment should not be changed")
def test_update_comment_post_id(helper_comments, new_comment_payload, faker_fixture, create_valid_post):
    """Test that updating the postId of a comment should not be allowed."""
    new_comment_payload[CommentFields.POST_ID.value] = create_valid_post[PostFields.ID.value]
    created_comment = helper_comments.create_comment(payload=new_comment_payload)

    updated_payload = {
        CommentFields.BODY.value: faker_fixture.sentence(nb_words=8),
        CommentFields.POST_ID.value: str(NONEXISTENT_ID)  # attempt to change to a different post
    }

    updated_comment = helper_comments.update_comment(
        comment_id=created_comment[CommentFields.ID.value],
        payload=updated_payload,
        expected_status=HTTPStatusCodes.BAD_REQUEST.value
    )
    pytest.logger.info(f"Attempted to update comment postId: {updated_comment}")
    assert updated_comment[CommentFields.POST_ID.value] == created_comment[CommentFields.POST_ID.value]


@pytest.mark.comments
@pytest.mark.negative
@pytest.mark.flaky_regression
def test_update_nonexistent_comment_fails(helper_comments, new_comment_payload):
    """Ensure that updating a nonexistent comment fails."""
    helper_comments.update_comment(
        comment_id=NONEXISTENT_ID,
        payload=new_comment_payload,
        expected_status=HTTPStatusCodes.NOT_FOUND.value
    )


@pytest.mark.comments
@pytest.mark.flaky_regression
def test_delete_comment(helper_comments, new_comment_payload):
    """Ensure that a comment can be deleted."""
    created_comment = helper_comments.create_comment(payload=new_comment_payload)

    deleted_comment = helper_comments.delete_comment(comment_id=created_comment[CommentFields.ID.value])
    pytest.logger.info(f"Deleted comment: {deleted_comment}")

    helper_comments.get_comment_by_id(comment_id=created_comment[CommentFields.ID.value], expected_status=HTTPStatusCodes.NOT_FOUND.value, expect_json=False)


@pytest.mark.comments
@pytest.mark.flaky_regression
def test_delete_nonexistent_comment_fails(helper_comments):
    """Ensure that deleting a nonexistent comment fails."""
    helper_comments.delete_comment(
        comment_id=NONEXISTENT_ID,
        expected_status=HTTPStatusCodes.NOT_FOUND.value,
        expect_json=False
    )


@pytest.mark.comments
@pytest.mark.negative
@pytest.mark.flaky_regression
@pytest.mark.parametrize(
    "payload, is_update, expected_status, test_title", NEGATIVE_COMMENT_PAYLOADS
)
def test_comment_payloads_negative_cases(helper_comments, payload, is_update, expected_status, test_title,
                                         create_valid_post, new_comment_payload):
    """Test invalid comment creation payloads."""
    pytest.logger.info(f"Running test {test_title}")
    if is_update:
        new_comment_payload[CommentFields.POST_ID.value] = create_valid_post[PostFields.ID.value]
        created_comment = helper_comments.create_comment(payload=new_comment_payload)
        helper_comments.update_comment(
            comment_id=created_comment[CommentFields.ID.value],
            payload=payload,
            expected_status=HTTPStatusCodes.BAD_REQUEST.value
        )
    else:
        pytest.logger.info(f"Running test {test_title}")
        helper_comments.create_comment(payload=payload, expected_status=expected_status)
