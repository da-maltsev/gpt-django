from a12n.api import views

from django.urls import path

app_name = "a12n"
urlpatterns = [
    path("token/", views.ObtainJSONWebTokenView.as_view()),
    path("token/refresh/", views.RefreshJSONWebTokenView.as_view()),
]
