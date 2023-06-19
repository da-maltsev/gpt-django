import pytest

from app.exceptions import AppServiceException
from gpt.models import Reply
from gpt.services.v1 import ChatCompleter

pytestmark = [
    pytest.mark.django_db,
]

previous_question = "Hello!"
previous_answer = "Hi there! How can I help you?"


@pytest.fixture
def openai_chat_completer():
    current_messages = [
        {"role": "user", "content": previous_question},
        {"role": "assistant", "content": previous_answer},
        {"role": "user", "content": "Why are you so serious?"},
    ]
    return ChatCompleter(current_messages=current_messages)


@pytest.fixture
def reply(factory, user):
    factory.cycle(3).reply(user=user, previous_reply=None)
    return factory.reply(
        author=user,
        question=previous_question,
        answer=previous_answer,
    )


def test_act_with_user(openai_chat_completer, user):
    openai_chat_completer.user = user

    new_messages = openai_chat_completer()

    assert len(new_messages) == 4
    assert new_messages[-1]["content"] == "test response"


def test_act_with_user_creates_reply(openai_chat_completer, user):
    openai_chat_completer.user = user

    result = openai_chat_completer()

    reply = Reply.objects.get()
    assert reply.author == user
    assert not reply.previous_reply
    assert reply.question == result[-2]["content"]
    assert reply.answer == result[-1]["content"]


def test_act_with_user_creates_reply_with_links_if_there_is_previous(openai_chat_completer, user, reply):
    openai_chat_completer.user = user

    openai_chat_completer()

    new_reply = Reply.objects.all().first()
    assert new_reply.previous_reply == reply
    assert reply.next_reply == new_reply


def test_act_without_user(openai_chat_completer):
    new_messages = openai_chat_completer()

    assert len(new_messages) == 4
    assert new_messages[-1]["content"] == "test response"


def test_act_with_error(openai_chat_completer, open_ai_mock):
    open_ai_mock.side_effect = AppServiceException("OpenAI error")

    with pytest.raises(AppServiceException, match="OpenAI error"):
        openai_chat_completer()
