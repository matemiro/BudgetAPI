from rest_framework import serializers

from app.models import Budget
from utils import pop_null_values_from_dict
from users.serializers import UserUsernameSerializer


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


class BudgetRetrieveSerializer(serializers.ModelSerializer):

    shared_with = UserUsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Budget
        fields = (
            "id",
            "name",
            "description",
            "shared_with",
        )
