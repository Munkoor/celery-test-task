import time

import requests


def get_with_retry(
    url: str, attempt_count: int = 3, cooldown: float = 5, **kwargs
) -> requests.Response:
    last_response = None
    for _ in range(attempt_count):
        last_response = requests.get(url, **kwargs)
        if last_response.status_code < 400:
            return last_response
        else:
            time.sleep(cooldown)
    return last_response
