from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle

from app.api.throttling import ConfigurableThrottlingMixin


class AnonGETGptRateThrottle(ConfigurableThrottlingMixin, AnonRateThrottle):
    """Throttle for anon get gpt."""

    scope = "anon-get-gpt"


class AnonPOSTGptRateThrottle(ConfigurableThrottlingMixin, AnonRateThrottle):
    """Throttle for anon post gpt."""

    scope = "anon-post-gpt"


class UserGETGptRateThrottle(ConfigurableThrottlingMixin, UserRateThrottle):
    """Throttle for anon get gpt."""

    scope = "user-get-gpt"


class UserPOSTGptRateThrottle(ConfigurableThrottlingMixin, UserRateThrottle):
    """Throttle for anon post gpt."""

    scope = "user-post-gpt"
