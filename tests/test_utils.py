from app.utils import get_with_retry


def test_get_with_retry_success(requests_mock):
    url = "https://fake.api"
    requests_mock.get(url, status_code=200, json={"data": "ok"})

    response = get_with_retry(url)
    assert response.status_code == 200
    assert response.json() == {"data": "ok"}


def test_get_with_retry_fails_after_retries(requests_mock):
    url = "https://fail.api"
    requests_mock.get(url, status_code=500)

    response = get_with_retry(url, attempt_count=2, cooldown=0)
    assert response.status_code == 500
