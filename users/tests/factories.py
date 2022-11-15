import factory

from users.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):

    email = factory.Faker("email")
    username = factory.Faker("user_name")
    password = factory.Faker(
        "password",
        length=12,
        digits=True,
        special_chars=True,
    )

    class Meta:
        model = CustomUser
