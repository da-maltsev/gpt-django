from django.urls import include, path
from gpt.api.v1 import viewsets
from rest_framework.routers import SimpleRouter

app_name = "gpt_rest"

router = SimpleRouter()
router.register("replies", viewsets.ReplyViewSet)


urlpatterns = [
    path("replies/count/", viewsets.RepliesCounterApiView.as_view()),
    path("", include(router.urls)),
    path("chat/", viewsets.OpenAiChatApiView.as_view()),
]
