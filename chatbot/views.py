from django.shortcuts import render, redirect
from .chatbot import custom_chatbot
from .forms import ChatbotForm
from .models import Chatbot


def chat_log(request):
    chats = Chatbot.objects.all()
    context = {"chats": chats}
    return render(request, "chatbot/chat_log.html", context)


def chatbot(request):
    if request.method == "POST":
        form = ChatbotForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data["user_message"]

            ai_response = custom_chatbot(user_message)

            messages = [{"role": "user", "content": user_message}]

            chat_history = Chatbot.objects.all()
            for chat in chat_history:
                messages.append({"role": "user", "content": chat.user_message})
                messages.append({"role": "assistant", "content": chat.ai_message})

            messages.append({"role": "assistant", "content": ai_response})

            chatbot = Chatbot(user_message=user_message, ai_message=ai_response)
            chatbot.save()

            return redirect("chatbot:log")
    else:
        form = ChatbotForm()
    context = {"form": form}
    return render(request, "chatbot/chatbot.html", context)
