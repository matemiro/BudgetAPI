from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.filters import CreatorFilterBackend
from app.models import Budget
from app.serializers import BudgetSerializer, BudgetRetrieveSerializer


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
