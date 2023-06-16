import pytest

from gpt.models import Reply
from gpt.services import MessageCreator

pytestmark = [
    pytest.mark.django_db,
]


def test_act_anon(session, anon_user):
    MessageCreator(session, anon_user, "test prompt", 0.1)()

    assert len(session["messages"]) == 3


def test_act_auth_creates_reply(session, user):
    MessageCreator(session, user, "test prompt", 0.1)()

    saved_reply = Reply.objects.get()
    assert saved_reply.question == "test prompt"
    assert saved_reply.answer == "test response"
    assert saved_reply.author == user
    assert saved_reply.status == Reply.Status.ACTIVE
    assert len(session["messages"]) == 3


def test_act_auth_creates_reply_with_links(session, user, reply):
    session["messages"] = [{"role": "system", "content": "sysysysy"}]
    session["messages"].append({"role": "user", "content": reply.question})
    session["messages"].append({"role": "assistant", "content": reply.answer})
    reply.setattr_and_save("status", Reply.Status.ACTIVE)

    MessageCreator(session, user, "test prompt", 0.1)()

    saved_reply = Reply.objects.first()
    assert saved_reply.previous_reply == reply
    assert reply.next_reply == saved_reply


def test_append_prompt_to_messages(session, anon_user):
    message_creator = MessageCreator(session, anon_user, "test prompt", 0.1)

    message_creator.append_prompt_to_messages()

    assert len(session["messages"]) == 2
    assert session["messages"][-1]["role"] == "user"
    assert session["messages"][-1]["content"] == "test prompt"


def test_add_response_to_message_list(session, anon_user):
    message_creator = MessageCreator(session, anon_user, "test prompt", 0.1)

    message_creator.add_response_to_message_list()

    assert len(session["messages"]) == 2
    assert session["messages"][1]["role"] == "assistant"
    assert session["messages"][1]["content"] == "test response"


def test_context_to_return(session, anon_user):
    message_creator = MessageCreator(session, anon_user, "test prompt", 0.1)

    result = message_creator.context_to_return

    assert isinstance(result, dict)
    assert "messages" in result
    assert "prompt" in result
    assert "temperature" in result
    assert result["prompt"] == ""
    assert result["temperature"] == 0.1
