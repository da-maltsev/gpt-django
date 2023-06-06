# importing the openai API
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from gpt.services import MessageCreator
from gpt.services import MessageDisplayer


def new_chat(request: HttpRequest) -> HttpResponse:
    # clear the messages list
    request.session.pop("messages", None)
    return redirect("gpt:home")


# this is the view for handling errors
def error_handler(request: HttpRequest) -> HttpResponse:
    return render(request, "assistant/404.html")


# this is the home view for handling home page logic
def home(request: HttpRequest) -> HttpResponse:
    try:
        if request.method == "POST":
            context = MessageCreator(
                session=request.session,
                prompt=request.POST.get("prompt", ""),
                temperature=float(request.POST.get("temperature", 0.1)),
            )()
            return render(request, "assistant/home.html", context)
        else:
            # if the request is not a POST request, render the home page
            context = MessageDisplayer(session=request.session)()
            return render(request, "assistant/home.html", context)
    except Exception as e:  # noqa PIE786
        return redirect("gpt:error_handler")
