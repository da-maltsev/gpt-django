import pytest

from pytest_lazyfixture import lazy_fixture

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    ("usages", "as_who"),
    [
        (0, lazy_fixture("as_anon")),
        (15, lazy_fixture("as_anon")),
        (9000, lazy_fixture("as_anon")),
        (0, lazy_fixture("as_user")),
        (15, lazy_fixture("as_user")),
        (9000, lazy_fixture("as_user")),
    ],
)
def test_correct_number(as_who, url_count, openai_profile, usages):
    openai_profile.setattr_and_save("usage_count", usages)

    got = as_who.get(url_count)

    assert got["count"] == usages
