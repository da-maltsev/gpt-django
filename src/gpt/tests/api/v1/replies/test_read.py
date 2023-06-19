import pytest

pytestmark = [
    pytest.mark.django_db,
]

BASE_URL: str = "/api/v1/replies/{reply_uuid}/"


@pytest.fixture
def url(reply) -> str:
    return BASE_URL.format(reply_uuid=reply.uuid)


def test_get_one(as_user, reply, url: str):
    got = as_user.get(url)

    assert got["uuid"] == str(reply.uuid)
    assert got["question"] == reply.question
    assert got["answer"] == reply.answer
    assert not got["previousReply"]
    assert not got["nextReply"]
    assert got["status"] == reply.status


def test_get_one_with_links(as_user, reply, url: str, factory):
    reply.previous_reply = factory.reply()
    factory.reply(previous_reply=reply)
    reply.save()

    got = as_user.get(url)

    assert got["previousReply"] == str(reply.previous_reply.uuid)
    assert got["nextReply"] == str(reply.next_reply.uuid)


def test_num_queries(as_user, url: str, django_assert_num_queries, reply, factory):
    reply.previous_reply = factory.reply()
    factory.reply(previous_reply=reply)
    reply.save()

    with django_assert_num_queries(2):
        as_user.get(url)
