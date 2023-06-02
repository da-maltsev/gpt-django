# importing the openai API
import openai

from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render

# import the generated API key from the secret_key file
# loading the API key from the secret_key file
openai.api_key = settings.OPENAI_TOKEN  # type: ignore[misc]


def new_chat(request):  # type: ignore
    # clear the messages list
    request.session.pop("messages", None)
    return redirect("gpt:home")


# this is the view for handling errors
def error_handler(request):  # type: ignore
    return render(request, "assistant/404.html")


# this is the home view for handling home page logic
def home(request):  # type: ignore
    try:
        # if the session does not have a messages key, create one
        if "messages" not in request.session:
            request.session["messages"] = [
                {"role": "Система", "content": "Задавайте осмысленные вопросы помогатору, не будьте сукой."},
            ]
        if request.method == "POST":
            # get the prompt from the form
            prompt = request.POST.get("prompt")
            # get the temperature from the form
            temperature = float(request.POST.get("temperature", 0.1))
            # append the prompt to the messages list
            request.session["messages"].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session["messages"],
                temperature=temperature,
                max_tokens=1000,
            )
            # format the response
            formatted_response = response["choices"][0]["message"]["content"]
            # append the response to the messages list
            request.session["messages"].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                "messages": request.session["messages"],
                "prompt": "",
                "temperature": temperature,
            }
            return render(request, "assistant/home.html", context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                "messages": request.session["messages"],
                "prompt": "",
                "temperature": 0.1,
            }
            return render(request, "assistant/home.html", context)
    except Exception as e:  # noqa PIE786
        print(e)  # noqa T201
        return redirect("gpt:error_handler")
