import uuid

from app.models import TimestampedModel

from django.db import models


class ReplyQuerySet(models.QuerySet):
    def for_viewset(self) -> "ReplyQuerySet":
        return self.select_related(
            "previous_reply",
            "next_reply",
        )


class Reply(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    objects = ReplyQuerySet.as_manager()

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    previous_reply = models.OneToOneField("self", null=True, related_name="next_reply", on_delete=models.SET_NULL)
    author = models.ForeignKey("users.User", related_name="replies", on_delete=models.CASCADE)

    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)

    class Meta:
        verbose_name_plural = "replies"
        ordering = ["-created"]


class OpenAiProfile(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    token = models.CharField(max_length=100, unique=True)
    usage_count = models.PositiveIntegerField(default=0)
    comment = models.TextField(default="")

    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)

    class Meta:
        ordering = ["-created"]
