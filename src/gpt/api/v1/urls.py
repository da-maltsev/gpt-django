from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from gpt.api.v1 import viewsets

app_name = "gpt_rest"

router = SimpleRouter()
router.register("replies", viewsets.ReplyViewSet)


urlpatterns = [
    path("replies/count/", viewsets.RepliesCounterApiView.as_view()),
    path("", include(router.urls)),
    path("chat/", viewsets.OpenAiChatApiView.as_view()),
]
