# Create your models here.
import uuid

from django.db import models

from app.models import TimestampedModel


class Reply(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    previous_reply = models.OneToOneField("self", null=True, related_name="next_reply", on_delete=models.SET_NULL)
    author = models.ForeignKey("users.User", related_name="replies", on_delete=models.CASCADE)

    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)

    class Meta:
        ordering = ["-created"]
