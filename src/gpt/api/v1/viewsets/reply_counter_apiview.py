from typing import Any

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from gpt.api.v1.serializers import ReplyCounterSerializer
from gpt.services.openai import OpenAiUsagesCounter


@extend_schema_view(
    get=extend_schema(
        responses={200: ReplyCounterSerializer}, tags=["replies"], description="Returns number of all questions that were made including anonymous."
    ),
)
class RepliesCounterApiView(APIView):
    permission_classes = ()

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        count = OpenAiUsagesCounter()()

        response_data = {
            "count": count,
        }
        return Response(ReplyCounterSerializer(response_data).data, status=status.HTTP_200_OK)
