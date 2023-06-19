import pytest

from gpt.services.openai.openai_usages_counter import OpenAiUsagesCounter

pytestmark = [
    pytest.mark.django_db,
]


def test_no_openai_profiles_return_zero():
    result = OpenAiUsagesCounter()()

    assert result == 0


def test_openai_profiles_zero_usages_return_zero(factory):
    factory.cycle(3).openai_profile(usage_count=0)

    result = OpenAiUsagesCounter()()

    assert result == 0


@pytest.mark.parametrize(
    ("profiles_quantity", "usages"),
    [
        (3, 5),
        (1, 10),
        (15, 1),
    ],
)
def test_openai_profiles_multiple_usages_return_sum(factory, profiles_quantity, usages):
    factory.cycle(profiles_quantity).openai_profile(usage_count=usages)
    sum_usages = profiles_quantity * usages

    result = OpenAiUsagesCounter()()

    assert result == sum_usages
