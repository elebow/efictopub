from unittest.mock import MagicMock

responses = []


def stub_response(html, *, status=200):
    responses.append(MagicMock(text=html, status=status))


def request_get(url, headers):
    # return_values must be populated by the consumer
    return responses.pop(0)
