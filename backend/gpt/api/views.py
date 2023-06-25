# importing the openai API
from typing import Any

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.decorators import throttle_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView

from gpt.api.throttle import AnonGETGptRateThrottle
from gpt.api.throttle import AnonPOSTGptRateThrottle
from gpt.api.throttle import UserGETGptRateThrottle
from gpt.api.throttle import UserPOSTGptRateThrottle
from gpt.models import Reply
from gpt.services import MessageCreator
from gpt.services import MessageCreatorException
from gpt.services import MessageDisplayer
from users.models import User


class ReplyListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Reply
    template_name = "assistant/reply_list.html"
    context_object_name = "replies"

    def get_queryset(self) -> models.QuerySet[Reply]:
        return Reply.objects.filter(author=self.request.user)  # type: ignore


class ReplyDetailView(DetailView):
    model = Reply
    template_name = "assistant/reply_detail.html"
    context_object_name = "reply"

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context["previous_page"] = self.request.META.get("HTTP_REFERER")
        return context


def new_chat(request: HttpRequest) -> HttpResponse:
    # clear the messages list
    user: User | AnonymousUser = request.user
    if isinstance(user, User):
        active_replies = user.replies.filter(status=Reply.Status.ACTIVE)
        for reply in active_replies:
            reply.status = Reply.Status.ARCHIVED
        Reply.objects.bulk_update(active_replies, ["status"])

    request.session.pop("messages", None)
    return redirect("gpt:home")


def error_handler(request: HttpRequest) -> HttpResponse:
    """this is the view for handling errors"""
    return render(request, "404.html")


def about_handler(request: HttpRequest) -> HttpResponse:
    """this is the view for about page"""
    return render(request, "about.html")


@api_view(["GET"])
@authentication_classes([SessionAuthentication])
@throttle_classes([AnonGETGptRateThrottle, UserGETGptRateThrottle])
@permission_classes([AllowAny])
def home(request: HttpRequest) -> HttpResponse:
    context = MessageDisplayer(session=request.session, user=request.user)()
    return render(request, "assistant/home.html", context)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@throttle_classes([AnonPOSTGptRateThrottle, UserPOSTGptRateThrottle])
@permission_classes([AllowAny])
def ask_gpt(request: HttpRequest) -> HttpResponse:
    try:
        context = MessageCreator(
            session=request.session,
            user=request.user,
            prompt=request.POST.get("prompt", ""),
            temperature=float(request.POST.get("temperature", 0.1)),
        )()
        return render(request, "assistant/home.html", context)
    except MessageCreatorException:
        return redirect("gpt:error_handler")
