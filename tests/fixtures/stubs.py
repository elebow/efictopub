from unittest.mock import MagicMock

responses = []


def stub_response(html, *, status=200):
    responses.append(MagicMock(text=html, status=status))


def request_get(url, headers):
    """Return a stubbed response that was previously set up by the consumer"""
    if len(responses) == 0:
        raise Exception(
            f"Tried to return stubbed response for {url}, but no stubbed responses left (or set up)."
        )

    return responses.pop(0)
