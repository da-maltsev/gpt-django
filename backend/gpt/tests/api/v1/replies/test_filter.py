import pytest
from freezegun import freeze_time
from gpt.models import Reply

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    ("created_after", "expected"),
    [
        ("2023-12-12", 0),
        ("1999-12-12", 1),
        ("2020-01-01", 1),
    ],
)
def test_created_after(as_user, user, factory, url_list, created_after, expected):
    with freeze_time("2020-01-01"):
        factory.reply(author=user)

    got = as_user.get(f"{url_list}?created_after={created_after}")["results"]

    assert len(got) == expected


@pytest.mark.parametrize(
    ("created_before", "expected"),
    [
        ("2023-12-12", 1),
        ("1999-12-12", 0),
        ("2020-01-01", 1),
    ],
)
def test_created_before(as_user, user, factory, url_list, created_before, expected):
    with freeze_time("2020-01-01"):
        factory.reply(author=user)

    got = as_user.get(f"{url_list}?created_before={created_before}")["results"]

    assert len(got) == expected


@pytest.mark.parametrize(
    ("created_before", "created_after", "expected"),
    [
        ("2023-12-12", "2019-12-12", 1),
        ("1999-12-12", "2030-12-12", 0),
        ("2020-01-01", "2020-01-01", 1),
        ("2015-01-01", "2012-01-01", 0),
    ],
)
def test_created_before_and_after(as_user, user, factory, url_list, created_before, created_after, expected):
    with freeze_time("2020-01-01"):
        factory.reply(author=user)

    got = as_user.get(f"{url_list}?created_before={created_before}&created_after={created_after}")["results"]

    assert len(got) == expected


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (Reply.Status.ARCHIVED, 2),
        (Reply.Status.ACTIVE, 1),
    ],
)
def test_status(as_user, status, user, factory, url_list, expected):
    with freeze_time("2020-01-01"):
        factory.reply(author=user, status=Reply.Status.ACTIVE)
        factory.cycle(2).reply(author=user, status=Reply.Status.ARCHIVED)

    got = as_user.get(f"{url_list}?status={status}")["results"]

    assert len(got) == expected


@pytest.mark.parametrize(
    ("created_before", "created_after", "status", "expected"),
    [
        ("2023-12-12", "2019-12-12", Reply.Status.ARCHIVED, 2),
        ("1999-12-12", "2030-12-12", Reply.Status.ARCHIVED, 0),
        ("2023-12-12", "2019-12-12", Reply.Status.ACTIVE, 1),
        ("1999-12-12", "2030-12-12", Reply.Status.ACTIVE, 0),
        ("2020-01-01", "2020-01-01", Reply.Status.ARCHIVED, 2),
        ("2015-01-01", "2012-01-01", Reply.Status.ARCHIVED, 0),
        ("2020-01-01", "2020-01-01", Reply.Status.ACTIVE, 1),
        ("2015-01-01", "2012-01-01", Reply.Status.ACTIVE, 0),
    ],
)
def test_created_before_and_after_and_status(as_user, status, user, factory, url_list, created_before, created_after, expected):
    with freeze_time("2020-01-01"):
        factory.reply(author=user, status=Reply.Status.ACTIVE)
        factory.cycle(2).reply(author=user, status=Reply.Status.ARCHIVED)

    got = as_user.get(f"{url_list}?created_before={created_before}&created_after={created_after}&status={status}")["results"]

    assert len(got) == expected
