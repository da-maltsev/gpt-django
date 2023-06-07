# importing the openai API
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.decorators import throttle_classes
from rest_framework.permissions import AllowAny

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from gpt.api.throttle import AnonGETGptRateThrottle
from gpt.api.throttle import AnonPOSTGptRateThrottle
from gpt.api.throttle import UserGETGptRateThrottle
from gpt.api.throttle import UserPOSTGptRateThrottle
from gpt.services import MessageCreator
from gpt.services import MessageDisplayer


def new_chat(request: HttpRequest) -> HttpResponse:
    # clear the messages list
    request.session.pop("messages", None)
    return redirect("gpt:home")


def error_handler(request: HttpRequest) -> HttpResponse:
    # this is the view for handling errors
    return render(request, "404.html")


@api_view(["GET"])
@authentication_classes([SessionAuthentication])
@throttle_classes([AnonGETGptRateThrottle, UserGETGptRateThrottle])
@permission_classes([AllowAny])
def home(request: HttpRequest) -> HttpResponse:
    context = MessageDisplayer(session=request.session)()
    return render(request, "assistant/home.html", context)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@throttle_classes([AnonPOSTGptRateThrottle, UserPOSTGptRateThrottle])
@permission_classes([AllowAny])
def ask_gpt(request: HttpRequest) -> HttpResponse:
    context = MessageCreator(
        session=request.session,
        prompt=request.POST.get("prompt", ""),
        temperature=float(request.POST.get("temperature", 0.1)),
    )()
    return render(request, "assistant/home.html", context)
