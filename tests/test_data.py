import pytest
from faker import Faker
from core import HTTPStatusCodes, PostFields, EXTRA_FIELD
faker_obj = Faker()

NEGATIVE_POST_PAYLOADS = [
    pytest.param(
        {PostFields.AUTHOR.value: "Author but missing Title"},
        False,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Missing title should fail",
        marks=pytest.mark.xfail(reason="POST missing title is not validated")
    ),
    pytest.param(
        {},
        False,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Empty payload should fail",
        marks=pytest.mark.xfail(reason="POST creation should not be created without payload")
    ),
    pytest.param(
        {PostFields.TITLE.value: "Title", PostFields.AUTHOR.value: "Author", EXTRA_FIELD: "extra"},
        False,
        HTTPStatusCodes.CREATED.value,
        "Creation with extra field should not be allowed",
    ),
    pytest.param(
        {PostFields.TITLE.value: "", PostFields.AUTHOR.value: "Author"},
        True,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Updating with empty title should fail",
        marks=pytest.mark.xfail(reason="Updating with empty title should fail but succeeds")
    ),
    pytest.param(
        {},
        True,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Updating with empty payload should fail",
        marks=pytest.mark.xfail(reason="Updating with empty payload should fail")
    )
]

NEGATIVE_COMMENT_PAYLOADS = [
    pytest.param(
        {"postId": 1},
        False,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Create comment with missing body",
        marks=pytest.mark.xfail(reason="COMMENT cannot be created without body")
    ),
    pytest.param(
        {"body": "Nice comment"},
        False,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Create comment with missing POST ID",
        marks=pytest.mark.xfail(reason="COMMENT cannot be created without postId")
    ),
    pytest.param(
        {"body": "Nice comment", "postId": faker_obj.random_int(min=1000, max=9999)},
        False,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Create comment with non-existent POST ID",
        marks=pytest.mark.xfail(reason="COMMENT cannot be created with non-existent POST ID")
    ),
    pytest.param(
        {"body": "", "postId": 1},
        False,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Create comment with empty body",
        marks=pytest.mark.xfail(reason="COMMENT cannot be created with empty payload")
    ),
    pytest.param(
        {},
        True,
        HTTPStatusCodes.BAD_REQUEST.value,
        "Create comment with empty body",
        marks=pytest.mark.xfail(reason="COMMENT cannot be updated with empty payload")
    ),

]

PROFILE_NEGATIVE_CASES = [
    pytest.param(
        {},
        HTTPStatusCodes.BAD_REQUEST.value,
        "Profile should not be updated with empty payload",
        marks=pytest.mark.skip(reason="PROFILE is updated with empty payload")
    ),
    pytest.param(
        {"name": ""},
        HTTPStatusCodes.BAD_REQUEST.value,
        "Profile should not be updated with empty name",
        marks=pytest.mark.skip(reason="PROFILE is updated with empty name")
    ),
    pytest.param(
        {"invalid_field": "unexpected"},
        HTTPStatusCodes.BAD_REQUEST.value,
        "Profile update with extra field should not be allowed",
        marks=pytest.mark.skip(reason="PROFILE is updated with extra field")
    )
]
