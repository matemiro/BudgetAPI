import pytest
from rest_framework.test import APIClient

from users.tests.factories import UserFactory


@pytest.fixture
def user(db, django_user_model):
    return UserFactory.create()


@pytest.fixture
def unauthenticated_user_client():
    return APIClient()


@pytest.fixture(scope="module")
def new_user_without_email_data():
    return {
        "username": "new_username",
        "password": "new_username",
    }


@pytest.fixture(scope="module")
def new_user_complete_data():
    return {
        "username": "new_username",
        "password": "password!for!user123",
        "email": "user@email.com",
    }


@pytest.fixture(scope="module")
def strong_password():
    return "1234sdkjfFSDFdlkfjlksSDFSFD!@#$"
