from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = "api_v1"
urlpatterns = [
    path("", include("gpt.api.v1.urls")),
    path("auth/", include("a12n.urls")),
    path("auth/", include("social_auth.urls")),
    path("users/", include("users.urls")),
    path("healthchecks/", include("django_healthchecks.urls")),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
]
