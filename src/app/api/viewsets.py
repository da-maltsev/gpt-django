from typing import Any, Protocol, Type

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

__all__ = [
    "ReadonlyModelViewSet",
]


class BaseGenericViewSet(Protocol):
    def get_serializer(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def get_response(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def perform_create(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def perform_update(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def get_success_headers(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def get_serializer_class(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def get_object(self, *args: Any, **kwargs: Any) -> Any:
        ...


class ResponseWithRetrieveSerializerMixin:
    """
    Always response with 'retrieve' serializer or fallback to `serializer_class`.
    Usage:

    class MyViewSet(DefaultModelViewSet):
        serializer_class = MyDefaultSerializer
        serializer_action_classes = {
           'list': MyListSerializer,
           'my_action': MyActionSerializer,
        }
        @action
        def my_action:
            ...

    'my_action' request will be validated with MyActionSerializer,
    but response will be serialized with MyDefaultSerializer
    (or 'retrieve' if provided).

    Thanks gonz: http://stackoverflow.com/a/22922156/11440

    """

    def get_response(self: BaseGenericViewSet, instance: Any, status: Any, headers: Any = None) -> Response:
        retrieve_serializer_class = self.get_serializer_class(action="retrieve")
        context = self.get_serializer_context()  # type: ignore
        retrieve_serializer = retrieve_serializer_class(instance, context=context)
        return Response(retrieve_serializer.data, status=status, headers=headers)

    def get_serializer_class(self: BaseGenericViewSet, action: str | None = None) -> Type[BaseSerializer]:
        if action is None:
            action = self.action  # type: ignore

        try:
            return self.serializer_action_classes[action]  # type: ignore
        except (KeyError, AttributeError):
            return super().get_serializer_class()  # type: ignore


class ReadonlyModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    GenericViewSet,
):
    pass
