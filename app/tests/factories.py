import factory
from factory.fuzzy import FuzzyChoice

from app.models import Budget, BudgetShares
from users.tests.factories import UserFactory


ROLE_CHOICES = [role[0] for role in BudgetShares.ROLES]


class BudgetFactory(factory.django.DjangoModelFactory):

    creator = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Budget {n}")
    description = factory.Faker("paragraph")

    class Meta:
        model = Budget
