from django.urls import path

from gpt.api.v1 import viewsets

app_name = "gpt_rest"


urlpatterns = [
    path("chat/", viewsets.OpenAiChatApiView.as_view()),
]
