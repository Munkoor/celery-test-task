import pytest
from unittest.mock import patch
from app.tasks import fetch_users, fetch_address, fetch_credit_card


@patch("app.tasks.user_services.add_user")
@patch("app.tasks.requests.get")
def test_fetch_users(mock_get, mock_add_user):
    mock_add_user.return_value = True
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"id": 1, "first_name": "Test", "last_name": "User", "email": "t@e.com"}
    ]

    result = fetch_users()
    assert result["status"] == "success"
    assert result["added_users"] == 1


@patch("app.tasks.get_with_retry")
@patch("app.tasks.user_services.get_users_without_address")
@patch("app.tasks.user_services.update_user_address")
def test_fetch_address(mock_update, mock_get_users, mock_retry):
    mock_get_users.return_value = [type("User", (), {"id": 1})()]
    mock_retry.return_value.status_code = 200
    mock_retry.return_value.json.return_value = [
        {"full_address": "123 Main St", "city": "X", "state": "Y", "country": "Z"}
    ]

    result = fetch_address()
    assert result["status"] == "success"
    assert result["updated"] == 1
