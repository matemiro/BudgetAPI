import json

import pytest
from django.urls import reverse

from app.models import Budget, BudgetShares
from app.tests.factories import (
    BudgetFactory,
    BudgetWithTwoReadOnlySharedUsersFactory,
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
