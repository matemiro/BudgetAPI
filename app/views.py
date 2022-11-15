from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.filters import CreatorFilterBackend
from app.models import Budget, CashFlowCategory
from app.permissions import (
    IsBudgetCreatorOrSharing,
    IsCategoryBudgetCreatorOrSharing,
)
from app.serializers import (
    BudgetSerializer,
    BudgetRetrieveSerializer,
    CashFlowCategoryCreateSerializer,
    CashFlowCategorySerializer,
)


class BudgetViewSet(ModelViewSet):

    queryset = Budget.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (CreatorFilterBackend,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BudgetRetrieveSerializer
        else:
            return BudgetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CashFlowCategoryViewSet(ModelViewSet):

    queryset = CashFlowCategory.objects.all()
    serializer_class = CashFlowCategorySerializer

    def get_permissions(self):
        permissions = [
            IsAuthenticated,
        ]
        if self.action in ["destroy", "retrieve", "partial_update", "update"]:
            permissions.append(IsCategoryBudgetCreatorOrSharing)
        else:
            permissions.append(IsBudgetCreatorOrSharing)

        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == "create":
            return CashFlowCategoryCreateSerializer
        else:
            return CashFlowCategorySerializer
