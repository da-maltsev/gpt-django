from rest_framework import serializers

from gpt.models import Reply


class ReplySerializer(serializers.ModelSerializer):
    previous_reply = serializers.SlugRelatedField(slug_field="uuid", queryset=Reply.objects.all(), allow_null=True)
    next_reply = serializers.SlugRelatedField(slug_field="uuid", queryset=Reply.objects.all(), allow_null=True)

    class Meta:
        model = Reply
        fields = (
            "uuid",
            "question",
            "answer",
            "previous_reply",
            "next_reply",
            "status",
            "created",
        )
