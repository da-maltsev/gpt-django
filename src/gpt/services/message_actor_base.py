from dataclasses import dataclass
from typing import Any

from django.contrib.sessions.backends.base import SessionBase

from app.services import BaseService


@dataclass
class MessageActorBase(BaseService):
    """Base class for messages"""

    session: SessionBase

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
