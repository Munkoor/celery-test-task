import os

import requests
from dotenv import load_dotenv
from celery import Celery, chain
from app.services import user_services
from app.db import Session
from app.utils import get_with_retry


load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
USERS_FETCH_SIZE = os.getenv("USERS_FETCH_SIZE")

app = Celery("tasks", broker=CELERY_BROKER_URL)


@app.task
def fetch_users():
    try:
        response = requests.get(
            "https://random-data-api.com/api/v2/users",
            params={"size": USERS_FETCH_SIZE},
        )
        response.raise_for_status()
        users_data = response.json()
        added = 0
        for user_data in users_data:
            if user_services.add_user(user_data):
                added += 1
        return {"status": "success", "added_users": added}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.task
def fetch_address(*args, **kwargs):
    try:
        with Session() as db:
            users = user_services.get_users_without_address(db)
            if not users:
                return {"status": "success", "message": "No users to update"}

            response = get_with_retry(
                "https://random-data-api.com/api/v2/addresses",
                params={"size": len(users)},
            )
            response.raise_for_status()
            addresses_data = response.json()

            for user in users:
                user_services.update_user_address(user, addresses_data.pop())

            db.commit()

        return {"status": "success", "updated": len(users)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.task
def fetch_credit_card(*args, **kwargs):
    try:
        with Session() as db:
            users = user_services.get_users_without_credit_card(db)
            if not users:
                return {"status": "success", "message": "No users to update"}

            response = get_with_retry(
                "https://random-data-api.com/api/v2/credit_cards",
                params={"size": len(users)},
            )
            response.raise_for_status()
            credit_cards_data = response.json()

            for user in users:
                user_services.update_user_credit_card(user, credit_cards_data.pop())

            db.commit()

        return {"status": "success", "updated": len(users)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.task
def full_pipeline():
    return chain(fetch_users.s(), fetch_address.s(), fetch_credit_card.s())()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(100.0, full_pipeline.s(), name="Run full pipeline")
