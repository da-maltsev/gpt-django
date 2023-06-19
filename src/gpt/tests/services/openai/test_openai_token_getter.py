import pytest

from django.conf import settings

from gpt.services.openai.openai_token_getter import OpenAiTokenGetter

pytestmark = [
    pytest.mark.django_db,
]


def test_act_without_active_model(openai_profile):
    openai_profile.setattr_and_save("status", "archived")

    result = OpenAiTokenGetter()()

    assert result == settings.OPENAI_TOKEN
    assert openai_profile.usage_count == 0


def test_act_with_active_model(openai_profile):
    openai_profile.setattr_and_save("status", "active")

    result = OpenAiTokenGetter()()

    openai_profile.refresh_from_db()
    assert result == openai_profile.token
    assert openai_profile.usage_count == 1
