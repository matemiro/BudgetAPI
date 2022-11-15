from rest_framework import serializers
from rest_framework.fields import CharField

from app.models import Budget, BudgetShares
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
