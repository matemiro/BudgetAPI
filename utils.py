from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Sum
from rest_framework import permissions

from app.models import Budget, BudgetShares, CashFlow

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


def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        from_email=None,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def get_users_budgets_summary(user: UserModel) -> dict:
    """
    Function that returns summary for each user's budgets.
    """
    budgets = Budget.objects.filter(creator=user).prefetch_related(
        "cashflow_set"
    )
    budgets_summary = dict()
    for budget in budgets:
        incomes = (
            budget.cashflow_set.filter(type=CashFlow.income).aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )
        expenses = (
            budget.cashflow_set.filter(type=CashFlow.expense).aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )
        total = incomes - expenses

        budgets_summary["incomes"] = float(incomes)
        budgets_summary["expenses"] = float(expenses)
        budgets_summary["total"] = float(total)

    return budgets_summary
