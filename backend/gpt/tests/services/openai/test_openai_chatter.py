import pytest

from django.conf import settings
from gpt.models import OpenAiProfile
from gpt.services.openai import OpenAiChatter
from gpt.services.openai import OpenAiChatterException
from gpt.services.openai.openai_chatter import EXCEEDED_SUBSCRIPTION_MESSAGE
from openai import OpenAIError

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def openai_profile(openai_profile):
    openai_profile.setattr_and_save("status", OpenAiProfile.Status.ACTIVE)
    return openai_profile


@pytest.fixture
def openai_chatter():
    messages = [
        {"role": "user", "content": "meow"},
        {"role": "assistant", "content": "woof"},
        {"role": "user", "content": "awoo"},
    ]
    return OpenAiChatter(messages)


@pytest.fixture
def mock_chat_completion(mocker):
    response_mock = {"choices": [{"message": {"content": "I'm fine, thank you."}}]}
    return mocker.patch("openai.ChatCompletion.create", return_value=response_mock)


def test_act_with_successful_response(openai_chatter, mock_chat_completion):
    response = openai_chatter()

    assert response == "I'm fine, thank you."


def test_act_with_exceeded_subscription_message(openai_chatter, mock_chat_completion, openai_profile):
    mock_chat_completion.side_effect = OpenAIError(EXCEEDED_SUBSCRIPTION_MESSAGE)

    with pytest.raises(OpenAiChatterException):
        openai_chatter()

    openai_profile.refresh_from_db()
    assert openai_profile.status == OpenAiProfile.Status.ARCHIVED


def test_act_with_other_error(openai_chatter, mock_chat_completion, openai_profile):
    mock_chat_completion.side_effect = OpenAIError("Ayyy lmao")

    with pytest.raises(OpenAiChatterException, match="Ayyy lmao"):
        openai_chatter()

    openai_profile.refresh_from_db()
    assert openai_profile.status == OpenAiProfile.Status.ACTIVE


def test_token_without_active_model(openai_profile, openai_chatter):
    openai_profile.setattr_and_save("status", "archived")

    result = openai_chatter.token

    assert result == settings.OPENAI_TOKEN
    assert openai_profile.usage_count == 0


def test_token_with_active_model(openai_profile, openai_chatter):
    openai_profile.setattr_and_save("status", "active")

    result = openai_chatter.token

    openai_profile.refresh_from_db()
    assert result == openai_profile.token
    assert openai_profile.usage_count == 1


@pytest.mark.parametrize("role", ["assistant", "system"])
def test_fail_if_last_message_not_from_user(openai_chatter, role):
    openai_chatter.messages.append(dict(role=role, content="nothing"))

    with pytest.raises(OpenAiChatterException, match="Last message must be question from user"):
        openai_chatter()
