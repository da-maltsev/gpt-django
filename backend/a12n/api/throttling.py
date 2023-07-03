from app.api.throttling import ConfigurableThrottlingMixin
from rest_framework.throttling import AnonRateThrottle


class AuthAnonRateThrottle(ConfigurableThrottlingMixin, AnonRateThrottle):
    """Throttle for any authorization views."""

    scope = "anon-auth"
