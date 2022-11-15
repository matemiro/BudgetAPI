from django.db import models

from users.models import CustomUser


class Budget(models.Model):

    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="budget_creator"
    )
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, default="")
    shared_with = models.ManyToManyField(
        CustomUser,
        through="BudgetShares",
        related_name="shared_with",
        blank=True,
    )


class BudgetShares(models.Model):

    ROLES = (
        (read_only := 1, "read_only"),
        (editor := 2, "editor"),
    )

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLES, default=read_only)

    class Meta:
        unique_together = (
            "budget",
            "shared_with",
        )


class CashFlowCategory(models.Model):

    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, default="")
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)


class CashFlow(models.Model):

    CASH_FLOW_TYPES = (
        (income := 1, "income"),
        (expense := 2, "expense"),
    )

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, default="")
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=CASH_FLOW_TYPES)
    category = models.ForeignKey(
        CashFlowCategory, null=True, blank=True, on_delete=models.SET_NULL
    )
