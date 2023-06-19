from dataclasses import dataclass
from typing import final

from gpt.models import Reply
from gpt.services.message_actor_base import MessageActorBase
from gpt.services.openai import OpenAiChatter
from users.models import User


class MessageCreatorException(Exception):
    """raises when it's impossible to create message"""


@final
@dataclass
class MessageCreator(MessageActorBase):
    """
    Sends question to OpenAI with context from previous messages
    which are stored in the Session object
    """

    prompt: str
    temperature: float

    def act(self) -> dict:
        """yep it uses a lot of state cause it works with Session"""
        self.append_prompt_to_messages()
        self.add_response_to_message_list()

        match self.user:
            case User():
                self.save_reply()

        return self.context_to_return

    def append_prompt_to_messages(self) -> None:
        """append the prompt to the messages list"""
        self.session["messages"].append({"role": "user", "content": self.prompt})
        self.session.modified = True

    def ask_open_ai(self) -> str:
        """call the openai API and get formatted response"""
        return OpenAiChatter(messages=self.session["messages"])()

    def add_response_to_message_list(self) -> None:
        """append the response to the messages list"""
        formatted_response = self.ask_open_ai()
        self.session["messages"].append({"role": "assistant", "content": formatted_response})
        self.session.modified = True

    def save_reply(self) -> Reply:
        """save reply to db and collect links to related replies if they exist"""
        question = self.session["messages"][-2]["content"]
        answer = self.session["messages"][-1]["content"]

        previous_reply = None
        if len(self.session["messages"]) >= 5:
            previous_question = self.session["messages"][-4]["content"]
            previous_answer = self.session["messages"][-3]["content"]
            previous_reply = self.user.replies.first()  # type: ignore
            if previous_reply:
                if previous_reply.answer != previous_answer or previous_reply.question != previous_question or previous_reply.status != Reply.Status.ACTIVE:
                    previous_reply = None

        return Reply.objects.create(
            author=self.user,  # type: ignore
            question=question,
            answer=answer,
            previous_reply=previous_reply,
        )
