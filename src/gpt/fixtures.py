import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.testing.factory import FixtureFactory
    from gpt.models import OpenAiProfile
    from gpt.models import Reply
    from users.models import User


@pytest.fixture
def reply(factory: "FixtureFactory", user: "User") -> "Reply":
    return factory.reply(author=user)


@pytest.fixture
def open_ai_profile(factory: "FixtureFactory") -> "OpenAiProfile":
    return factory.open_ai_profile(usage_count=0)
