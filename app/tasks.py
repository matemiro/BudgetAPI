import json

from celery import shared_task
from django.contrib.auth import get_user_model

from utils import get_users_budgets_summary, send_email

UserModel = get_user_model()


@shared_task
def send_emails_task():
    users = UserModel.objects.filter(
        premium_account=True, get_notification=True
    ).prefetch_related("budget_creator__cashflow_set")
    for user in users:
        users_budgets_summary = get_users_budgets_summary(user)
        send_email(
            "Your budgets summary",
            json.dumps(users_budgets_summary),
            [
                user.email,
            ],
        )
