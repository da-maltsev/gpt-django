from social_auth.api.viewsets import exchange_token

from django.urls import path

urlpatterns = [
    path("<str:backend>/", exchange_token),
]
