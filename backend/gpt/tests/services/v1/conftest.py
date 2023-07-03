import pytest


@pytest.fixture(autouse=True)
def open_ai_mock(mocker):
    return mocker.patch(
        "gpt.services.v1.ChatCompleter.ask_open_ai",
        return_value="test response",
    )
