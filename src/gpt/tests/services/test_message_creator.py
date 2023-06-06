import pytest

from gpt.services import MessageCreator

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture(autouse=True)
def _open_ai(mocker):
    mocker.patch(
        "gpt.services.MessageCreator.ask_open_ai",
        return_value="test response",
    )


def test_act(session):
    MessageCreator(session, "test prompt", 0.1)()

    assert len(session["messages"]) == 3


def test_append_prompt_to_messages(session):
    message_creator = MessageCreator(session, "test prompt", 0.1)

    message_creator.append_prompt_to_messages()

    assert len(session["messages"]) == 2
    assert session["messages"][-1]["role"] == "user"
    assert session["messages"][-1]["content"] == "test prompt"


def test_add_response_to_message_list(session):
    message_creator = MessageCreator(session, "test prompt", 0.1)

    message_creator.add_response_to_message_list()

    assert len(session["messages"]) == 2
    assert session["messages"][1]["role"] == "assistant"
    assert session["messages"][1]["content"] == "test response"


def test_context_to_return(session):
    message_creator = MessageCreator(session, "test prompt", 0.1)

    result = message_creator.context_to_return

    assert isinstance(result, dict)
    assert "messages" in result
    assert "prompt" in result
    assert "temperature" in result
    assert result["prompt"] == ""
    assert result["temperature"] == 0.1
