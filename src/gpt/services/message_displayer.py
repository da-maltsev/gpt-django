from django.utils.functional import cached_property

from gpt.services.message_actor_base import MessageActorBase


class MessageDisplayer(MessageActorBase):
    """Shows messages at home page"""

    def act(self) -> dict:
        return self.context_to_return

    @cached_property
    def context_to_return(self) -> dict:
        return {
            "messages": self.session["messages"],
            "prompt": "",
            "temperature": 0.1,
        }
