"""budget_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from users.views import CreateUserView

from rest_framework_simplejwt.views import (  # noqa, isort:skip
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from app.views import (  # noqa, isort:skip
    BudgetViewSet,
    CashFlowCategoryViewSet,
    CashFlowViewSet,
    BudgetSharesViewSet,
)

router = routers.DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budgets")
router.register(r"categories", CashFlowCategoryViewSet, basename="categories")
router.register(r"cash-flows", CashFlowViewSet, basename="cash_flows")
router.register(r"budget-share", BudgetSharesViewSet, basename="budget_share")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", CreateUserView.as_view(), name="register"),
    path("", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
