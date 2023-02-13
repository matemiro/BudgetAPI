import json

import pytest
from django.urls import reverse

from app.models import Budget, BudgetShares, CashFlowCategory
from users.tests.factories import UserFactory

from app.tests.factories import (  # noqa, isort:skip
    BudgetFactory,
    BudgetWithTwoReadOnlySharedUsersFactory,
    CashFlowCategoryFactory,
)


@pytest.mark.django_db
def test_unauthenticated_user_cant_get_budgets_list(
    unauthenticated_user_client,
):
    response = unauthenticated_user_client.get(reverse("budgets-list"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_get_budgets_list(authenticated_user_client, user):
    budgets = BudgetFactory.create_batch(creator=user, size=10)
    assert Budget.objects.filter(creator=user).count() == 10

    response = authenticated_user_client.get(reverse("budgets-list"))
    assert response.status_code == 200

    expected_response_data = [
        {
            "id": budget.id,
            "name": budget.name,
            "description": budget.description,
        }
        for budget in budgets
    ]
    assert response.json() == expected_response_data


@pytest.mark.django_db
def test_user_retrieve_budget_details(authenticated_user_client, user):
    budget = BudgetWithTwoReadOnlySharedUsersFactory.create(creator=user)
    url = reverse("budgets-detail", kwargs={"pk": budget.id})
    response = authenticated_user_client.get(url)

    assert response.status_code == 200

    budget_shares = BudgetShares.objects.filter(budget=budget).all()
    shares = [
        {
            "id": budget.id,
            "username": budget.shared_with.username,
            "role": budget.role,
        }
        for budget in budget_shares
    ]
    expected_response_data = {
        "id": budget.id,
        "name": budget.name,
        "description": budget.description,
        "creator": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        "shares": shares,
    }
    assert response.json() == expected_response_data


@pytest.mark.django_db
def test_user_create_budget(authenticated_user_client, user):
    BudgetFactory.create_batch(creator=user, size=10)
    users_budget_count = Budget.objects.filter(creator=user).count()
    assert users_budget_count == 10

    new_budget_name = "budget name"
    new_budget_description = "This is new budget description."
    response = authenticated_user_client.post(
        reverse("budgets-list"),
        data=json.dumps(
            {"name": new_budget_name, "description": new_budget_description}
        ),
        content_type="application/json",
    )
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["name"] == new_budget_name
    assert response_data["description"] == new_budget_description
    assert Budget.objects.filter(creator=user).count() == users_budget_count + 1


@pytest.mark.django_db
def test_unauthenticated_user_cant_create_budget(unauthenticated_user_client):
    new_budget_name = "budget name"
    new_budget_description = "This is new budget description."
    response = unauthenticated_user_client.post(
        reverse("budgets-list"),
        data=json.dumps(
            {"name": new_budget_name, "description": new_budget_description}
        ),
        content_type="application/json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_list_budget_categories(authenticated_user_client, user):
    budget = BudgetFactory.create(creator=user)
    CashFlowCategoryFactory.create_batch(size=5, budget=budget)
    assert CashFlowCategory.objects.filter(budget=budget).count() == 5

    response = authenticated_user_client.get(
        reverse("categories-list"), data={"budget": budget.id}
    )
    assert response.status_code == 200

    expected_response = [
        {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "budget": budget.id,
        }
        for category in CashFlowCategory.objects.filter(budget=budget)
    ]
    assert response.json() == expected_response


@pytest.mark.django_db
def test_unauthenticated_user_cant_list_budget_categories(
    unauthenticated_user_client,
):
    url = reverse("categories-list")
    response = unauthenticated_user_client.get(url, data={"budget": 1})
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_cant_list_foreign_categories(authenticated_user_client):
    budget = BudgetFactory.create(creator=UserFactory.create())
    response = authenticated_user_client.get(
        reverse("categories-list"), data={"budget": budget.id}
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_list_provided_categories(authenticated_user_client, user):
    budget = BudgetFactory.create(creator=UserFactory.create())
    budget.shared_with.add(user)

    CashFlowCategoryFactory.create_batch(size=3, budget=budget)

    response = authenticated_user_client.get(
        reverse("categories-list"), data={"budget": budget.id}
    )
    assert response.status_code == 200

    expected_response = [
        {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "budget": budget.id,
        }
        for category in CashFlowCategory.objects.filter(budget=budget)
    ]
    assert response.json() == expected_response
