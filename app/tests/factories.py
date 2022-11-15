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


class BudgetSharesFactory(factory.django.DjangoModelFactory):

    budget = factory.SubFactory(BudgetFactory)
    shared_with = factory.SubFactory(UserFactory)
    role = FuzzyChoice(ROLE_CHOICES)

    class Meta:
        model = BudgetShares


class ReadOnlyBudgetSharesFactory(BudgetSharesFactory):

    role = BudgetShares.read_only


class EditorBudgetSharesFactory(BudgetSharesFactory):

    role = BudgetShares.editor


class BudgetWithTwoReadOnlySharedUsersFactory(BudgetFactory):
    sharing1 = factory.RelatedFactory(
        ReadOnlyBudgetSharesFactory, factory_related_name="budget"
    )
    sharing2 = factory.RelatedFactory(
        ReadOnlyBudgetSharesFactory, factory_related_name="budget"
    )
