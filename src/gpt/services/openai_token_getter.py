from dataclasses import dataclass

from django.conf import settings
from django.db.models import F

from app.services import BaseService
from gpt.models import OpenAiProfile


@dataclass
class OpenAiTokenGetter(BaseService):
    """
    Chooses token from db if there are active tokens
    else takes default token from env
    """

    def act(self) -> str:
        active_open_ai_profile = OpenAiProfile.objects.filter(status=OpenAiProfile.Status.ACTIVE).first()
        if active_open_ai_profile:
            active_open_ai_profile.usage_count = F("usage_count") + 1
            active_open_ai_profile.save()
            return active_open_ai_profile.token
        return settings.OPENAI_TOKEN  # type: ignore[misc]
