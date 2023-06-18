from dataclasses import dataclass
from typing import Callable, Type

import openai
from openai import OpenAIError

from django.utils.functional import cached_property

from app.exceptions import AppServiceException
from app.services import BaseService
from gpt.models import Reply
from gpt.services.openai_token_getter import OpenAiTokenGetter
from users.models import User

TEMPERATURE = 0.1  # at this moment it's fine to always use default temperature


class OpenAiChatCompleterException(AppServiceException):
    """raises when it's impossible to complete chat"""


@dataclass
class OpenAiChatCompleter(BaseService):
    """
    Gets current messages, and answers to last question
    Sends question to OpenAI with context from previous messages

    If there is user, saves its messages to db
    """

    current_messages: list[dict]
    user: User | None = None

    def act(self) -> list[dict]:
        answer = self.ask_open_ai()

        if self.user:
            self.save_reply(self.user, self.question, answer)

        new_messages = self.current_messages.copy()
        new_messages.append(dict(role="assistant", content=answer))

        return new_messages

    def ask_open_ai(self) -> str:
        """call the openai API and get formatted response"""
        try:
            response = self.open_ai_client_completion.create(
                model="gpt-3.5-turbo",
                messages=self.current_messages,
                temperature=TEMPERATURE,
                max_tokens=1000,
                request_timeout=25,
            )
            return response["choices"][0]["message"]["content"]
        except OpenAIError as e:
            self.current_messages.pop()
            raise OpenAiChatCompleterException(e)

    def save_reply(self, user: User, question: str, answer: str) -> Reply:
        """save reply to db and collect links to related replies if they exist"""
        previous_reply = user.replies.first()

        if previous_reply and self.valid_messages_for_creating_reply_with_link:
            previous_reply_equal_last_messages = previous_reply.answer == self.previous_answer and previous_reply.question == self.previous_question

            if not previous_reply_equal_last_messages:
                previous_reply = None

        return Reply.objects.create(
            author=user,
            question=question,
            answer=answer,
            previous_reply=previous_reply,
        )

    @cached_property
    def open_ai_client_completion(self) -> Type[openai.ChatCompletion]:
        openai.api_key = OpenAiTokenGetter()()

        return openai.ChatCompletion

    @cached_property
    def question(self) -> str:
        return self.current_messages[-1]["content"]

    @cached_property
    def valid_messages_for_creating_reply_with_link(self) -> bool:
        with_system_message = len(self.current_messages) >= 4 and self.current_messages[0]["role"] == "system"
        without_system_message = len(self.current_messages) >= 3 and self.current_messages[0]["role"] == "user"
        return with_system_message or without_system_message

    @cached_property
    def previous_question(self) -> str | None:
        if not self.valid_messages_for_creating_reply_with_link:
            return None
        return self.current_messages[-3]["content"]

    @cached_property
    def previous_answer(self) -> str | None:
        if not self.valid_messages_for_creating_reply_with_link:
            return None
        return self.current_messages[-2]["content"]

    def get_validators(self) -> list[Callable]:
        return [self.validate_last_message_is_question]

    def validate_last_message_is_question(self) -> None:
        last_message = self.current_messages[-1]
        if last_message["role"] != "user":
            raise OpenAiChatCompleterException("Last message must be question from user")
