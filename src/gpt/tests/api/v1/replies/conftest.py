import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def url_list() -> str:
    return "/api/v1/replies/"


@pytest.fixture
def url_count() -> str:
    return "/api/v1/replies/count/"


@pytest.fixture
def url_read(reply) -> str:
    return f"/api/v1/replies/{reply.uuid}/"


@pytest.fixture
def url_set_archived() -> str:
    return "/api/v1/replies/status/archived/"
