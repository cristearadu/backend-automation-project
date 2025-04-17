import requests


def http_request(method, url, headers=None, json=None, files=None):
    return requests.request(method=method, url=url, headers=headers, json=json, files=files)
