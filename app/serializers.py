from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.generics import get_object_or_404

from app.models import Budget, BudgetShares, CashFlow, CashFlowCategory
from users.serializers import UserSerializer
from utils import pop_null_values_from_dict


class BudgetSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Budget
        fields = (
            "id",
            "creator",
            "name",
            "description",
        )

    def to_representation(self, instance):
        """
        Prevent situation to set category witch not belongs to edited budget.
        """
        representation = super().to_representation(instance)
        return pop_null_values_from_dict(representation)


class BudgetSharesSerializer(serializers.ModelSerializer):
    username = CharField(source="shared_with.username", read_only=True)

    class Meta:
        model = BudgetShares
        fields = (
            "id",
            "username",
            "role",
        )


class CashFlowsTotalBalanceSerializer(serializers.ModelSerializer):
    incomes = serializers.SerializerMethodField()
    expenses = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = CashFlow
        fields = ("incomes", "expenses", "total")

    def get_incomes(self, cash_flows):
        return (
            cash_flows.filter(type=CashFlow.income).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

    def get_expenses(self, cash_flows):
        return (
            cash_flows.filter(type=CashFlow.expense).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

    def get_total(self, cash_flows):
        return cash_flows.aggregate(Sum("amount"))["amount__sum"] or 0


class BudgetRetrieveSerializer(serializers.ModelSerializer):
    shares = BudgetSharesSerializer(source="budgetshares_set", many=True)
    creator = UserSerializer()
    total_balance = CashFlowsTotalBalanceSerializer(source="cashflow_set")

    class Meta:
        model = Budget
        fields = (
            "id",
            "name",
            "description",
            "creator",
            "shares",
            "total_balance",
        )


class CashFlowCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowCategory
        fields = ("id", "name", "description", "budget")


class CashFlowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowCategory
        fields = ("id", "name", "description", "budget")
        extra_kwargs = {"budget": {"read_only": True}}


class CashFlowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = ("id", "name", "amount", "type", "category")
        extra_kwargs = {"category": {"read_only": True}}


class CashFlowDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = (
            "id",
            "amount",
            "name",
            "description",
            "budget",
            "type",
            "category",
        )
        extra_kwargs = {
            "budget": {"read_only": True},
            "category": {"read_only": True},
        }


class CashFlowCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = (
            "id",
            "amount",
            "name",
            "description",
            "budget",
            "type",
            "category",
        )

    def validate(self, data):
        """
        Prevent situation to set category witch not exist in budget.
        """

        budget = data.get("budget")
        category = data.get("category")

        if not category:
            return data

        if not category.budget == budget:
            raise ValidationError("No such category in budget.")

        return data


class CashFlowPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = (
            "id",
            "amount",
            "name",
            "description",
            "budget",
            "type",
            "category",
        )
        extra_kwargs = {
            "budget": {"read_only": True, "required": False},
            "type": {"required": False},
            "name": {"required": False},
            "amount": {"required": False},
        }

    def validate_category(self, category):
        """
        Prevent situation to set category witch not belongs to edited budget.
        """
        budget = get_object_or_404(
            CashFlow, pk=self.context["view"].kwargs["pk"]
        ).budget
        if not category.budget == budget:
            raise ValidationError("No such category in budget.")
        return category


class BudgetShareCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetShares
        fields = ("id", "budget", "shared_with", "role")

    def validate_shared_with(self, user):
        """
        Checking if the budget is not shared with the budget creator.
        """

        if user == self.context["request"].user:
            raise ValidationError("Can't share with budget creator.")
        return user


class BudgetSharePartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetShares
        fields = ("id", "budget", "shared_with", "role")
        extra_kwargs = {
            "budget": {"read_only": True},
            "shared_with": {"read_only": True},
        }
