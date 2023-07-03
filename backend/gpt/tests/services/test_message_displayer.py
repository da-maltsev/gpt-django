import pytest

from gpt.services import MessageDisplayer

pytestmark = [
    pytest.mark.django_db,
]


def test_act_anon(session, anon_user):
    result = MessageDisplayer(session, anon_user)()

    assert isinstance(result, dict)
    assert "messages" in result
    assert "prompt" in result
    assert "temperature" in result
    assert "usage_count" in result


def test_act_auth(session, user):
    result = MessageDisplayer(session, user)()

    assert isinstance(result, dict)
    assert "messages" in result
    assert "prompt" in result
    assert "temperature" in result
    assert "usage_count" in result


def test_context_to_return_no_messages(session, anon_user):
    result = MessageDisplayer(session, anon_user).context_to_return

    assert isinstance(result, dict)
    assert "messages" in result
    assert "prompt" in result
    assert "temperature" in result
    assert "usage_count" in result
