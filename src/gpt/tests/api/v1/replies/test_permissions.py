import pytest

from pytest_lazyfixture import lazy_fixture
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    ("method", "url", "expected_status"),
    [
        ("get", lazy_fixture("url_list"), status.HTTP_401_UNAUTHORIZED),
        ("get", lazy_fixture("url_read"), status.HTTP_401_UNAUTHORIZED),
        ("post", lazy_fixture("url_set_archived"), status.HTTP_401_UNAUTHORIZED),
        ("get", lazy_fixture("url_count"), status.HTTP_200_OK),
    ],
)
def test_what_anon_can(as_anon, method, url, expected_status):
    getattr(as_anon, method)(url, expected_status=expected_status)
