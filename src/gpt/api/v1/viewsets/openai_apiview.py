from typing import Any

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from gpt.api.throttle import AnonPOSTGptRateThrottle
from gpt.api.throttle import UserPOSTGptRateThrottle
from gpt.api.v1.serializers import ChatSerializer
from gpt.services.v1 import OpenAiChatCompleter
from users.models import User


@extend_schema_view(
    post=extend_schema(responses={201: ChatSerializer}, request=ChatSerializer, tags=["chat"]),
)
class OpenAiChatApiView(APIView):
    throttle_classes = [AnonPOSTGptRateThrottle, UserPOSTGptRateThrottle]
    permission_classes = ()

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_messages = serializer.validated_data.copy()
        user_or_none = self.get_user_or_none(request)

        messages_with_answer = OpenAiChatCompleter(current_messages.get("messages"), user_or_none)()

        response_data = {
            "messages": messages_with_answer,
        }
        return Response(ChatSerializer(response_data).data, status=status.HTTP_201_CREATED)

    def get_user_or_none(self, request: Request) -> User | None:
        if request.user.is_authenticated:
            return request.user
