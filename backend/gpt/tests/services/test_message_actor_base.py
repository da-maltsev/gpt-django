import pytest

from gpt.services.message_actor_base import MessageActorBase

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def messages() -> list[dict]:
    return [{"hello": "it's me"}]


def test_post_init(session, anon_user):
    MessageActorBase(session, anon_user)

    assert "messages" in session
    assert session["messages"] == [
        {
            "role": "system",
            "content": "На осмысленные вопросы будет дан осмысленный ответ.",
        },
    ]


def test_context_to_return_with_messages(session, anon_user, messages):
    session.update({"messages": messages})

    result = MessageActorBase(session, anon_user).context_to_return

    assert result.get("messages") == messages


def test_context_to_return_with_correct_usage_count(session, anon_user, openai_profile):
    openai_profile.setattr_and_save("usage_count", 15)

    result = MessageActorBase(session, anon_user).context_to_return

    assert result.get("usage_count") == 15
