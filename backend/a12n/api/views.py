from a12n.api.throttling import AuthAnonRateThrottle
from rest_framework_jwt import views as jwt


class ObtainJSONWebTokenView(jwt.ObtainJSONWebTokenView):
    throttle_classes = [AuthAnonRateThrottle]


class RefreshJSONWebTokenView(jwt.RefreshJSONWebTokenView):
    throttle_classes = [AuthAnonRateThrottle]
