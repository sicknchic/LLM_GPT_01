# LLM_GPT_01

## 기본과제
```python
# chatbot/main.py
import openai
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# API ket 설정
openai.api_key = os.getenv("OPENAI_API_KEY")


def custom_chatbot():
    prompt = "You're someone who shares kind and comforting words with people feeling tired or stressed."

    messages = [{"role": "system", "content": prompt}]

    chat_log = "chat_log.txt"

    with open(chat_log, "w", encoding="utf-8") as log_file:
        log_file.write("Chat Log:\n")
        log_file.write(f"prompt: {prompt}\n")
        log_file.write("-----" * 20 + "\n")

    while True:
        user_message = input("메세지를 입력해주세요. (종료: exit): ")

        if user_message.lower() == "exit":
            print("대화를 종료합니다.")
            break

        messages.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        ai_response = response["choices"][0]["message"]["content"]

        messages.append({"role": "assistant", "content": ai_response})

        with open(chat_log, "a", encoding="utf-8") as log_file:
            log_file.write(f"사용자: {user_message}\n")
            log_file.write(f"Chatbot: {ai_response}\n")
            log_file.write("-----" * 20 + "\n")

        print(f"system: {ai_response}")


custom_chatbot()

```
## 도전과제
```python
import openai
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# API ket 설정
openai.api_key = os.getenv("OPENAI_API_KEY")


def custom_chatbot(user_message):
# chatbot/chatbot.py
    prompt = "You're someone who shares kind and comforting words with people feeling tired or stressed."

    messages = [{"role": "system", "content": prompt}]

    messages.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    ai_response = response["choices"][0]["message"]["content"]

    return ai_response

```

```python
# chatbot/models.py
from django.db import models
from django.conf import settings


class Chatbot(models.Model):
    user_message = models.TextField()
    ai_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.pk)}번째 대화"

```

```python
# chatbot/forms.py
from django import forms
from .models import Chatbot


class ChatbotForm(forms.ModelForm):
    class Meta:
        model = Chatbot
        fields = ["user_message"]

```

```python
# chatbot/views.py
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
```