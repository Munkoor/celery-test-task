from app.services import user_services
from app.models import User


def test_add_user_adds_new_user(db_session, monkeypatch):
    monkeypatch.setattr(user_services, "Session", lambda: db_session)

    user_data = {
        "id": 1,
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
    }

    added = user_services.add_user(user_data)
    assert added is True

    users = db_session.query(User).all()
    assert len(users) == 1
    assert users[0].name == "Test User"


def test_add_user_does_not_duplicate(db_session, monkeypatch):
    monkeypatch.setattr(user_services, "Session", lambda: db_session)

    user_data = {
        "id": 1,
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
    }
    user_services.add_user(user_data)
    added = user_services.add_user(user_data)
    assert added is False
