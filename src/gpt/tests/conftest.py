import pytest

from django.contrib.sessions.backends.base import SessionBase

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def session() -> SessionBase:
    return SessionBase()
