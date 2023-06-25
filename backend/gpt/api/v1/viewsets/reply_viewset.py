from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import QuerySet

from app.api.viewsets import ReadonlyModelViewSet
from gpt.api.v1.filtersets import ReplyFilterSet
from gpt.api.v1.serializers import ReplySerializer
from gpt.models import Reply


@extend_schema(tags=["replies"])
class ReplyViewSet(ReadonlyModelViewSet):
    queryset = Reply.objects.for_viewset()
    filterset_class = ReplyFilterSet
    permission_classes = [IsAuthenticated]

    lookup_field = "uuid"
    serializer_class = ReplySerializer

    @extend_schema(request=None, responses=None, description="Must be used to set archived status to all user's replies")
    @action(methods=["POST"], url_path="status/archived", detail=False)
    def archive_reply(self, *args: Any, **kwargs: Any) -> Response:
        self.queryset.update(status=Reply.Status.ARCHIVED)
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self) -> QuerySet[Reply]:
        return super().get_queryset().filter(author=self.request.user)
