from dataclasses import dataclass
from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.base import SessionBase

from app.services import BaseService
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
                    "content": "На осмысленные вопросы будет дан осмысленный ответ. На глупые вопросы будет дан анекдот про армян и нарды.",
                },
            ]

    def act(self) -> Any:
        ...
