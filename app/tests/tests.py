import pytest
from django.urls import reverse

from app.tests.factories import BudgetFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_unauthenticated_user_cant_get_budgets_list(
    unauthenticated_user_client,
):

    response = unauthenticated_user_client.get(reverse("budgets-list"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_get_budgets_list(authenticated_user_client, user):

    budget = BudgetFactory(creator=user)
    users_to_share = [UserFactory.create() for _ in range(3)]
    for user_to_share in users_to_share:
        budget.shared_with.add(user_to_share)

    response = authenticated_user_client.get(reverse("budgets-list"))

    assert response.status_code == 200
