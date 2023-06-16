import pytest

from django.conf import settings

from gpt.services.openai_token_getter import OpenAiTokenGetter

pytestmark = [
    pytest.mark.django_db,
]


def test_act_without_active_model(open_ai_profile):
    open_ai_profile.setattr_and_save("status", "archived")

    result = OpenAiTokenGetter()()

    assert result == settings.OPENAI_TOKEN
    assert open_ai_profile.usage_count == 0


def test_act_with_active_model(open_ai_profile):
    open_ai_profile.setattr_and_save("status", "active")

    result = OpenAiTokenGetter()()

    open_ai_profile.refresh_from_db()
    assert result == open_ai_profile.token
    assert open_ai_profile.usage_count == 1
