from dataclasses import dataclass
from typing import Type

import openai
from openai import OpenAIError

from django.conf import settings
from django.utils.functional import cached_property

from gpt.services.message_actor_base import MessageActorBase


@dataclass
class MessageCreator(MessageActorBase):
    """
    Sends question to OpenAI with context from previous messages
    which are stored in the Session object
    """

    prompt: str
    temperature: float

    def act(self) -> dict:
        # yep it uses a lot of state cause it works with Session
        self.append_prompt_to_messages()
        self.add_response_to_message_list()
        return self.context_to_return

    def append_prompt_to_messages(self) -> None:
        # append the prompt to the messages list
        self.session["messages"].append({"role": "user", "content": self.prompt})
        self.session.modified = True

    def ask_open_ai(self) -> str:
        # call the openai API and get formatted response
        try:
            response = self.open_ai_client_completion.create(
                model="gpt-3.5-turbo",
                messages=self.session["messages"],
                temperature=self.temperature,
                max_tokens=1000,
            )
            return response["choices"][0]["message"]["content"]
        except OpenAIError as e:
            return f"Error while handling request to OpenAI:\n{e}"

    def add_response_to_message_list(self) -> None:
        # append the response to the messages list
        formatted_response = self.ask_open_ai()
        self.session["messages"].append({"role": "assistant", "content": formatted_response})
        self.session.modified = True

    @cached_property
    def context_to_return(self) -> dict:
        return {
            "messages": self.session["messages"],
            "prompt": "",
            "temperature": self.temperature,
        }

    @cached_property
    def open_ai_client_completion(self) -> Type[openai.ChatCompletion]:
        # import the generated API key from the secret_key file
        # loading the API key from the secret_key file
        openai.api_key = settings.OPENAI_TOKEN  # type: ignore[misc]

        return openai.ChatCompletion
