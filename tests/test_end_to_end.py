import pytest
from schemas import PostModel, CommentModel
from core import HTTPStatusCodes, CommentFields, PostFields


@pytest.mark.e2e
@pytest.mark.posts
@pytest.mark.comments
@pytest.mark.flaky_regression
def test_create_post_and_comment(helper_posts, helper_comments, new_post_payload, new_comment_payload):
    """Test the full flow: create post -> create comment on post -> validate comment.
    """
    pytest.logger.info("# Step 1: Create a new post")
    created_post = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info(f"Created post: {created_post}")

    # Validate created post schema
    post_obj = PostModel(**created_post)

    pytest.logger.info("# Step 2: Create a comment related to the post")
    new_comment_payload[CommentFields.POST_ID.value] = post_obj.id
    created_comment = helper_comments.create_comment(payload=new_comment_payload)
    pytest.logger.info(f"Created comment: {created_comment}")

    # Validate created comment schema
    comment_obj = CommentModel(**created_comment)

    pytest.logger.info("# Step 3: Fetch the comment by ID and validate contents")
    fetched_comment = helper_comments.get_comment_by_id(comment_id=comment_obj.id)
    assert fetched_comment[CommentFields.POST_ID.value] == post_obj.id, \
        (f"Comment postId does not match the created post ID. Expected response: {post_obj.id}. "
         f"Actual response:{fetched_comment[CommentFields.POST_ID.value]}")
    assert fetched_comment[CommentFields.BODY.value] == new_comment_payload[CommentFields.BODY.value], \
        (f"Comment body does not match payload. Expected response: {new_comment_payload[CommentFields.BODY.value]}. "
         f"Actual response:{fetched_comment[CommentFields.BODY.value]}")


@pytest.mark.e2e
@pytest.mark.comments
@pytest.mark.flaky_regression
def test_create_update_delete_comment(helper_posts, helper_comments, new_post_payload, new_comment_payload,
                                      faker_fixture):
    """Test the full flow: create post -> create comment -> update comment -> delete comment -> validate deletion.
    """
    pytest.logger.info("# Step 1: Create a new post")
    created_post = helper_posts.create_post(payload=new_post_payload)
    pytest.logger.info(f"Created post: {created_post}")

    pytest.logger.info("# Step 2: Create a new comment on that post")
    new_comment_payload[CommentFields.POST_ID.value] = created_post["id"]
    created_comment = helper_comments.create_comment(payload=new_comment_payload)
    pytest.logger.info(f"Created comment: {created_comment}")

    # Validate created comment schema
    comment_obj = CommentModel(**created_comment)

    pytest.logger.info("# Step 3: Update the comment body")
    updated_payload = {
        CommentFields.BODY.value: faker_fixture.sentence(nb_words=10),
        CommentFields.POST_ID.value: created_post["id"],
    }
    updated_comment = helper_comments.update_comment(comment_id=comment_obj.id, payload=updated_payload)
    pytest.logger.info(f"Updated comment: {updated_comment}")

    # Validate updated fields
    assert updated_comment[CommentFields.BODY.value] == updated_payload[CommentFields.BODY.value], \
        (f"Updated comment body mismatch. Expected: {updated_payload[CommentFields.BODY.value]}, "
         f"Actual: {updated_comment[CommentFields.BODY.value]}")

    pytest.logger.info("# Step 4: Delete the comment")
    deleted_comment = helper_comments.delete_comment(comment_id=comment_obj.id)
    pytest.logger.info(f"Deleted comment: {deleted_comment}")

    pytest.logger.info("# Step 5: Attempt to fetch deleted comment (should result in 404)")
    helper_comments.get_comment_by_id(comment_id=comment_obj.id, expected_status=404, expect_json=False)


@pytest.mark.e2e
@pytest.mark.posts
@pytest.mark.comments
@pytest.mark.flaky_regression
def test_create_multiple_posts_and_comments(helper_posts, helper_comments, new_post_payload, new_comment_payload):
    """Create multiple posts and comments, then validate postId relations."""
    posts = []
    pytest.logger.info("# Step 1: Create multiple posts")
    for _ in range(2):
        post = helper_posts.create_post(payload=new_post_payload)
        posts.append(PostModel(**post))
        pytest.logger.info(f"Created post: {post}")

    comments = []
    pytest.logger.info("# Step 2: Create multiple comments for the created posts")
    for post in posts:
        new_comment_payload[CommentFields.POST_ID.value] = post.id
        comment = helper_comments.create_comment(payload=new_comment_payload)
        comments.append(CommentModel(**comment))
        pytest.logger.info(f"Created comment for post {post.id}: {comment}")

    pytest.logger.info("# Step 3: Validate comments are linked to correct posts")
    for comment, post in zip(comments, posts):
        assert comment.postId == post.id, f"Comment postId mismatch. Expected: {post.id}, Actual: {comment.postId}"


@pytest.mark.e2e
@pytest.mark.posts
@pytest.mark.comments
@pytest.mark.flaky_regression
def test_update_post_with_existing_comments(helper_posts, helper_comments, new_post_payload, new_comment_payload, faker_fixture):
    """Create a post with comments, update the post, and validate comments are still linked."""
    post = helper_posts.create_post(payload=new_post_payload)
    post_obj = PostModel(**post)
    pytest.logger.info(f"Created post: {post_obj}")

    pytest.logger.info("# Step 1: Create comment attached to post")
    new_comment_payload[CommentFields.POST_ID.value] = post_obj.id
    comment = helper_comments.create_comment(payload=new_comment_payload)
    comment_obj = CommentModel(**comment)
    pytest.logger.info(f"Created comment: {comment_obj}")

    pytest.logger.info("# Step 2: Update the post")
    updated_payload = {
        PostFields.TITLE.value: faker_fixture.sentence(nb_words=5),
        PostFields.AUTHOR.value: faker_fixture.name()
    }
    updated_post = helper_posts.update_post(post_id=post_obj.id, payload=updated_payload)
    pytest.logger.info(f"Updated post: {updated_post}")

    pytest.logger.info("# Step 3: Fetch the comment again")
    fetched_comment = helper_comments.get_comment_by_id(comment_id=comment_obj.id)
    assert fetched_comment[CommentFields.POST_ID.value] == post_obj.id, \
        (f"Fetched comment postId mismatch after post update. Expected: {post_obj.id}, "
         f"Actual: {fetched_comment[CommentFields.POST_ID.value]}")


@pytest.mark.e2e
@pytest.mark.posts
@pytest.mark.comments
@pytest.mark.flaky_regression
def test_delete_post_and_validate_comments(helper_posts, helper_comments, new_post_payload, new_comment_payload):
    """Create post, comment, delete post, and try fetching comment."""
    post = helper_posts.create_post(payload=new_post_payload)
    post_obj = PostModel(**post)
    pytest.logger.info(f"Created post: {post_obj}")

    pytest.logger.info("# Step 1: Create comment attached to post")
    new_comment_payload[CommentFields.POST_ID.value] = post_obj.id
    comment = helper_comments.create_comment(payload=new_comment_payload)
    comment_obj = CommentModel(**comment)
    pytest.logger.info(f"Created comment: {comment_obj}")

    pytest.logger.info("# Step 2: Delete the post")
    deleted_post = helper_posts.delete_post(post_id=post_obj.id)
    pytest.logger.info(f"Deleted post: {deleted_post}")

    pytest.logger.info("# Step 3: Try fetching the comment")
    fetched_comment = helper_comments.get_comment_by_id(comment_id=comment_obj.id, expected_status=HTTPStatusCodes.OK.value)
    pytest.logger.info(f"Fetched comment after post deletion: {fetched_comment}")

    pytest.logger.info("# Step 4: Validate the comment still exists (JSON Server behavior)")
    assert fetched_comment[CommentFields.ID.value] == comment_obj.id, \
        f"Expected comment ID {comment_obj.id}, got {fetched_comment[CommentFields.ID.value]}"
