import pytest
from django.urls import reverse

from users.models import CustomUser


@pytest.mark.django_db
def test_register_user(unauthenticated_user_client, new_user_complete_data):
    response = unauthenticated_user_client.post(
        reverse("register"), data=new_user_complete_data
    )

    assert response.status_code == 201
    assert CustomUser.objects.count() == 1

    user = CustomUser.objects.first()
    assert user.username == new_user_complete_data["username"]
    assert user.email == new_user_complete_data["email"]


@pytest.mark.django_db
def test_register_user_without_email(
    unauthenticated_user_client, new_user_without_email_data
):
    response = unauthenticated_user_client.post(
        reverse("register"), data=new_user_without_email_data
    )

    assert response.status_code == 201
    assert CustomUser.objects.count() == 1

    user = CustomUser.objects.first()
    assert user.username == new_user_without_email_data["username"]
    assert user.email == ""


@pytest.mark.django_db
def test_cant_register_user_with_existing_username(
    unauthenticated_user_client, user, strong_password
):
    existing_username = user.username
    response = unauthenticated_user_client.post(
        reverse("register"),
        data={
            "username": existing_username,
            "password": strong_password,
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_cant_register_user_with_existing_email(
    unauthenticated_user_client, user, strong_password
):
    existing_email = user.email
    response = unauthenticated_user_client.post(
        reverse("register"),
        data={
            "username": "notexistingusername",
            "email": existing_email,
            "password": strong_password,
        },
    )
    assert response.status_code == 400
