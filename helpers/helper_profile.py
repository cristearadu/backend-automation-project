from core import BlogApiEndpointKeys, HTTPStatusCodes
from .helper import Helper


class HelperProfile(Helper):
    def __init__(self):
        super().__init__()

    def get_profile(self, expected_status=HTTPStatusCodes.OK.value):
        return self._send_request(BlogApiEndpointKeys.GET_PROFILE, expected_status)

    def update_profile(self, payload: dict, expected_status=HTTPStatusCodes.OK.value):
        return self._send_request(BlogApiEndpointKeys.UPDATE_PROFILE, expected_status, payload=payload)
