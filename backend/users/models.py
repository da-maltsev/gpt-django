from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models

if TYPE_CHECKING:
    from gpt.models import Reply


class User(AbstractUser):
    objects = _UserManager()  # type: _UserManager

    replies: models.QuerySet["Reply"]
