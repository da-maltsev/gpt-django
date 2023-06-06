import pytest

from gpt.services import MessageDisplayer

pytestmark = [
    pytest.mark.django_db,
]


def test_act(session):
    result = MessageDisplayer(session)()

    assert isinstance(result, dict)
    assert "messages" in result
    assert "prompt" in result
    assert "temperature" in result


def test_context_to_return(session):
    result = MessageDisplayer(session).context_to_return

    assert isinstance(result, dict)
    assert "messages" in result
    assert "prompt" in result
    assert "temperature" in result
