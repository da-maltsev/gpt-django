from dataclasses import dataclass
from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.utils.functional import cached_property

from app.services import BaseService
from gpt.services.openai_usages_counter import OpenAiUsagesCounter
from users.models import User


@dataclass
class MessageActorBase(BaseService):
    """Base class for messages"""

    session: SessionBase
    user: User | AnonymousUser

    def __post_init__(self) -> None:
        if "messages" not in self.session:
            self.session["messages"] = [
                {
                    "role": "system",
                    "content": "На осмысленные вопросы будет дан осмысленный ответ.",
                },
            ]

    def act(self) -> Any:
        ...

    @cached_property
    def context_to_return(self) -> dict:
        return {
            "messages": self.session["messages"],
            "prompt": "",
            "temperature": 0.1,
            "usage_count": self.usage_count,
        }

    @cached_property
    def usage_count(self) -> int:
        return OpenAiUsagesCounter()()
