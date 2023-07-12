from drf_spectacular.utils import extend_schema
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from social_auth.api.serializers import SocialSerializer
from social_django.utils import psa


@extend_schema(request=SocialSerializer)
@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):  # type: ignore
    """
    Exchange an OAuth2 access token for one for this site.
    """
    serializer = SocialSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = request.backend.do_auth(serializer.validated_data["access_token"])
    except HTTPError as e:
        return Response(
            {
                "errors": {
                    "token": "Invalid token",
                    "detail": str(e),
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user:
        if user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(
            {"errors": "This user account is inactive"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"errors": "Authentication Failed"},
        status=status.HTTP_400_BAD_REQUEST,
    )
