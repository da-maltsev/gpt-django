from rest_framework import serializers

from gpt.definitions import OPENAI_ROLES


class ChatMessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=OPENAI_ROLES, required=True)
    content = serializers.CharField(min_length=1, max_length=1000, required=True)


class ChatSerializer(serializers.Serializer):
    messages = serializers.ListField(child=ChatMessageSerializer(), required=True)
