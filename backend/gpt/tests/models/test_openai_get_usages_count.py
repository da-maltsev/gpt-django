import pytest
from gpt.models import OpenAiProfile

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def get_counters():
    return lambda: OpenAiProfile.objects.get_usages_count()


def test_no_openai_profiles_return_zero(get_counters):
    result = get_counters()

    assert result == 0


def test_openai_profiles_zero_usages_return_zero(factory, get_counters):
    factory.cycle(3).openai_profile(usage_count=0)

    result = get_counters()

    assert result == 0


@pytest.mark.parametrize(
    ("profiles_quantity", "usages"),
    [
        (3, 5),
        (1, 10),
        (15, 1),
    ],
)
def test_openai_profiles_multiple_usages_return_sum(factory, profiles_quantity, usages, get_counters):
    factory.cycle(profiles_quantity).openai_profile(usage_count=usages)
    sum_usages = profiles_quantity * usages

    result = get_counters()

    assert result == sum_usages
