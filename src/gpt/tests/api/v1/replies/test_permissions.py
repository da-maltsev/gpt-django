import pytest

from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]


def test_anon_cant_list(as_anon):
    as_anon.get("/api/v1/replies/", expected_status=status.HTTP_401_UNAUTHORIZED)


def test_anon_cant_read(as_anon, reply):
    url = f"/api/v1/replies/{reply.uuid}/"

    as_anon.get(url, expected_status=status.HTTP_401_UNAUTHORIZED)


def test_anon_cant_archived(as_anon, reply):
    url = "/api/v1/replies/status/archived/"

    as_anon.post(url, expected_status=status.HTTP_401_UNAUTHORIZED)
