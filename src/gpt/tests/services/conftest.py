import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.base import SessionBase

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def session() -> SessionBase:
    return SessionBase()


@pytest.fixture(autouse=True)
def open_ai_mock(mocker):
    return mocker.patch(
        "gpt.services.MessageCreator.ask_open_ai",
        return_value="test response",
    )


@pytest.fixture
def anon_user() -> AnonymousUser:
    return AnonymousUser()
