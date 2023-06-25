from dataclasses import dataclass
from typing import Callable, final, Type

import openai
from openai import OpenAIError

from django.utils.functional import cached_property

from app.exceptions import AppServiceException
from app.services import BaseService
from gpt.models import OpenAiProfile
from gpt.services.openai.openai_token_getter import OpenAiTokenGetter

TEMPERATURE = 0.1  # at this moment it's fine to always use default temperature
TIMEOUT = 25
MAX_TOKENS = 1000
EXCEEDED_SUBSCRIPTION_MESSAGE = "You exceeded your current quota, please check your plan and billing details."


class OpenAiChatterException(AppServiceException):
    """raises when it's impossible to chat with openai"""


@final
@dataclass
class OpenAiChatter(BaseService):
    messages: list[dict]

    def act(self) -> str:
        self.set_token()

        try:
            answer = self.ask_open_ai(self.messages)
        except OpenAIError as e:
            if str(e) == EXCEEDED_SUBSCRIPTION_MESSAGE:
                self.archivate_openai_profile(self.token)
            raise OpenAiChatterException(e)

        return answer

    def set_token(self) -> None:
        openai.api_key = self.token

    def archivate_openai_profile(self, token: str) -> None:
        openai_profile = OpenAiProfile.objects.filter(token=token).first()
        if openai_profile:
            openai_profile.setattr_and_save("status", OpenAiProfile.Status.ARCHIVED)

    def ask_open_ai(self, messages: list[dict]) -> str:
        """call the openai API and get formatted response"""
        response = self.chat_completion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            request_timeout=TIMEOUT,
        )
        return response["choices"][0]["message"]["content"]

    @cached_property
    def chat_completion(self) -> Type[openai.ChatCompletion]:
        return openai.ChatCompletion

    @cached_property
    def token(self) -> str:
        return OpenAiTokenGetter()()

    def get_validators(self) -> list[Callable]:
        return [self.validate_last_message_is_question]

    def validate_last_message_is_question(self) -> None:
        last_message = self.messages[-1]
        if last_message["role"] != "user":
            raise OpenAiChatterException("Last message must be question from user")
