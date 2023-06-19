import pytest

pytestmark = [
    pytest.mark.django_db,
]

BASE_URL: str = "/api/v1/replies/"


@pytest.fixture
def url() -> str:
    return BASE_URL


def test_without_entities(as_user, url):
    got = as_user.get(url)

    assert got["results"] == []


def test_have_required_fields(as_user, url, reply, factory, user):
    reply.previous_reply = factory.reply()
    factory.reply(previous_reply=reply)
    reply.save()

    got = as_user.get(url)["results"][0]

    assert got["uuid"] == str(reply.uuid)
    assert got["question"] == str(reply.question)
    assert got["answer"] == str(reply.answer)
    assert got["previousReply"] == str(reply.previous_reply.uuid)
    assert got["nextReply"] == str(reply.next_reply.uuid)
    assert got["status"] == reply.status


def test_num_queries(as_user, django_assert_num_queries, user, factory, url):
    factory.cycle(6).reply(author=user)
    factory.reply()

    with django_assert_num_queries(3):
        as_user.get(url)
