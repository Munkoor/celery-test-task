from app.models import User
from app.db import Session


def add_user(user_data):
    with Session() as db:
        user_id = user_data["id"]
        if not db.query(User).filter(User.id == user_id).first():
            new_user = User(
                id=user_id,
                name=f"{user_data['first_name']} {user_data['last_name']}",
                email=user_data["email"],
            )
            db.add(new_user)
            db.commit()
            return True
        return False


def get_users_without_address(db):
    return db.query(User).filter(User.address.is_(None)).all()


def get_users_without_credit_card(db):
    return db.query(User).filter(User.credit_card.is_(None)).all()


def update_user_address(user, address_data):
    user.address = (
        f"{address_data['full_address']}, {address_data['city']}, "
        f"{address_data['state']}, {address_data['country']}"
    )


def update_user_credit_card(user, card_data):
    user.credit_card = card_data["credit_card_number"]
