from typing import TYPE_CHECKING

from app.testing import register

if TYPE_CHECKING:
    from app.testing.types import FactoryProtocol
    from gpt.models import OpenAiProfile
    from gpt.models import Reply


@register
def reply(self: "FactoryProtocol", **kwargs: dict) -> "Reply":
    return self.mixer.blend("gpt.Reply", **kwargs)


@register
def open_ai_profile(self: "FactoryProtocol", **kwargs: dict) -> "OpenAiProfile":
    return self.mixer.blend("gpt.OpenAiProfile", **kwargs)
