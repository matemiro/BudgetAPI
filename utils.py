from django.contrib.auth import get_user_model
from rest_framework import permissions

from app.models import Budget, BudgetShares

UserModel = get_user_model()


def pop_null_values_from_dict(data: dict) -> dict:
    return {key: value for key, value in data.items() if value}


def has_user_budget_permission(
    user: UserModel, budget: Budget, request_method: str
):
    try:
        share = BudgetShares.objects.get(budget=budget, shared_with=user)
    except BudgetShares.DoesNotExist:
        return False

    if (share.role == BudgetShares.editor) or (
        request_method in permissions.SAFE_METHODS
    ):
        return True

    return False
