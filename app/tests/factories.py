import factory
from factory.fuzzy import FuzzyChoice

from app.models import Budget, BudgetShares, CashFlow, CashFlowCategory
from users.tests.factories import UserFactory

ROLE_CHOICES = [role[0] for role in BudgetShares.ROLES]
CASH_FLOW_TYPES = [
    cashflow_type[0] for cashflow_type in CashFlow.CASH_FLOW_TYPES
]


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


class CashFlowCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("paragraph")
    budget = factory.SubFactory(BudgetFactory)

    class Meta:
        model = CashFlowCategory


class CashFlowFactory(factory.django.DjangoModelFactory):
    amount = factory.Faker(
        "pydecimal", left_digits=18, right_digits=2, positive=True
    )
    name = factory.Sequence(lambda n: f"CashFlow {n}")
    description = factory.Faker("paragraph")
    budget = factory.SubFactory(BudgetFactory)
    type = FuzzyChoice(CASH_FLOW_TYPES)
    category = factory.SubFactory(
        CashFlowCategoryFactory, budget=factory.SelfAttribute("..budget")
    )
