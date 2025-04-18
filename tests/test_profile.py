import pytest
from core import HTTPStatusCodes
from schemas import ProfileModel
from helpers.helper_profile import HelperProfile
from pydantic_core._pydantic_core import ValidationError
from test_data import PROFILE_NEGATIVE_CASES


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
@pytest.mark.parametrize("payload, test_title, expected_status", PROFILE_NEGATIVE_CASES)
def test_update_profile_negative_cases(helper_profile, payload, test_title, expected_status):
    """Test negative scenarios for updating profile."""
    pytest.logger.info(f"Running test {test_title}")
    helper_profile.update_profile(
        payload=payload,
        expected_status=expected_status
    )
