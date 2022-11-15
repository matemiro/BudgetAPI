from rest_framework import serializers
from rest_framework.fields import CharField

from app.models import Budget, BudgetShares, CashFlowCategory
from utils import pop_null_values_from_dict
from users.serializers import UserSerializer


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


class BudgetRetrieveSerializer(serializers.ModelSerializer):

    shares = BudgetSharesSerializer(source="budgetshares_set", many=True)
    creator = UserSerializer()

    class Meta:
        model = Budget
        fields = (
            "id",
            "name",
            "description",
            "creator",
            "shares",
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
