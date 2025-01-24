from django.urls import path
from . import views

app_name = "chatbot"
urlpatterns = [
    path("log/", views.chat_log, name="log"),
    path("", views.chatbot, name="chatbot"),
]
