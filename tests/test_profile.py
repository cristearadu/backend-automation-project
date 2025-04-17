import pytest
from core import HTTPStatusCodes
from schemas import ProfileModel
from helpers.helper_profile import HelperProfile
from pydantic_core._pydantic_core import ValidationError


@pytest.mark.smoke
@pytest.mark.profile
@pytest.mark.flaky_regression
def test_get_profile(helper_profile):
    """Verify that GET /profile returns the profile info."""
    profile_data = helper_profile.get_profile()
    pytest.logger.info(f"Fetched profile: {profile_data}")
    assert profile_data["name"], "Profile 'name' field should not be empty"


@pytest.mark.smoke
@pytest.mark.profile
@pytest.mark.flaky_regression
def test_get_profile(helper_profile):
    """Verify that GET /profile response conforms to the defined schema."""
    try:
        ProfileModel(**helper_profile.get_profile())
    except ValidationError as e:
        pytest.logger.error(f"PostModel response schema has failed: {e}")
        pytest.fail(f"Schema validation failed for PostModel: {e}")


@pytest.mark.profile
@pytest.mark.flaky_regression
def test_update_profile(faker_fixture):
    """Verify that PUT /profile can update the profile name."""
    helper = HelperProfile()
    new_name = faker_fixture.company()
    updated_profile = helper.update_profile(payload={"name": new_name})
    pytest.logger.info(f"Updated profile: {updated_profile}")
    assert updated_profile["name"] == new_name, \
        f"Profile name was not updated correctly. Expected {new_name}. Actual profile name: {updated_profile['name']}"


@pytest.mark.profile
@pytest.mark.negative
@pytest.mark.flaky_regression
@pytest.mark.xfail(reason="Profile update negative cases (empty payload, invalid fields, empty name)")
@pytest.mark.parametrize(
    "payload",
    [
        {},  # Empty payload
        {"name": ""},  # Empty name
        {"invalid_field": "unexpected"},  # Invalid extra field
    ],
    ids=[
        "empty_payload",
        "empty_name",
        "invalid_field"
    ]
)
def test_update_profile_negative_cases(payload):
    """Test negative scenarios for updating profile."""
    helper = HelperProfile()
    helper.update_profile(payload=payload, expected_status=HTTPStatusCodes.BAD_REQUEST.value)