from typing import final

from gpt.services.message_actor_base import MessageActorBase


@final
class MessageDisplayer(MessageActorBase):
    """Shows messages at home page"""

    def act(self) -> dict:
        return self.context_to_return
