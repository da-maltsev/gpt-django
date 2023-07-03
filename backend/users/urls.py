from users.api import viewsets

from django.urls import path

app_name = "users"
urlpatterns = [
    path("me/", viewsets.SelfView.as_view()),
]
