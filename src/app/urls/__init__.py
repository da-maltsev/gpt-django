from django.contrib import admin
from django.urls import include
from django.urls import path

api = [
    path("v1/", include("app.urls.v1", namespace="v1")),
]

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(api)),
    path("", include("gpt.urls")),
]
