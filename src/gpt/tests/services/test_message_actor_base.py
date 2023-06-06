import pytest

from gpt.services.message_actor_base import MessageActorBase

pytestmark = [
    pytest.mark.django_db,
]


def test_post_init(session):
    MessageActorBase(session)

    assert "messages" in session
    assert session["messages"] == [
        {
            "role": "system",
            "content": "На осмысленные вопросы будет дан осмысленный ответ. На глупые вопросы будет дан анекдот про армян и нарды.",
        },
    ]
