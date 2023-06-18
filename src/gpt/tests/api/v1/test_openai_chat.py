import pytest

from rest_framework import status

from gpt.models import Reply
from gpt.services.v1.openai_chat_completer import OpenAiChatCompleterException

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture(autouse=True)
def open_ai_mock(mocker):
    return mocker.patch(
        "gpt.services.v1.OpenAiChatCompleter.ask_open_ai",
        return_value="woof",
    )


url: str = "/api/v1/chat/"


@pytest.fixture()
def messages() -> list[dict]:
    return [
        {
            "role": "system",
            "content": "meow",
        },
        {
            "role": "user",
            "content": "meow",
        },
        {
            "role": "assistant",
            "content": "meow",
        },
        {
            "role": "user",
            "content": "meow",
        },
    ]


def test_success_as_user(as_user, messages):
    result = as_user.post(url, data=dict(messages=messages))

    assert result["messages"] == [*messages, {"role": "assistant", "content": "woof"}]


def test_success_anon(as_anon, messages):
    result = as_anon.post(url, data=dict(messages=messages))

    assert result["messages"] == [*messages, {"role": "assistant", "content": "woof"}]


def test_success_as_user_creates_reply(as_user, user, messages):
    as_user.post(url, data=dict(messages=messages))

    reply = Reply.objects.get()
    assert reply.question == "meow"
    assert reply.answer == "woof"
    assert reply.author == user


def test_fail_if_last_message_not_from_user_role(as_user, messages):
    messages.append(dict(role="assistant", content="awoo"))

    as_user.post(url, data=dict(messages=messages), expected_status=status.HTTP_400_BAD_REQUEST)


def test_fail_if_openai_return_error(as_user, messages, open_ai_mock):
    open_ai_mock.side_effect = OpenAiChatCompleterException("(((")

    as_user.post(url, data=dict(messages=messages), expected_status=status.HTTP_400_BAD_REQUEST)
