from rest_framework import permissions

from app.models import Budget
from utils import has_user_budget_permission


class IsBudgetCreatorOrSharing(permissions.BasePermission):
    def has_permission(self, request, view):
        budget_id = request.data.get("budget") or request.query_params.get(
            "budget"
        )
        try:
            budget = Budget.objects.get(pk=budget_id)
        except Budget.DoesNotExist:
            return False
        except ValueError:
            return False

        if request.user == budget.creator:
            return True

        return has_user_budget_permission(
            user=request.user, budget=budget, request_method=request.method
        )


class IsObjectsBudgetCreatorOrSharing(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        budget = obj.budget

        if request.user == budget.creator:
            return True

        return has_user_budget_permission(
            user=request.user, budget=budget, request_method=request.method
        )
