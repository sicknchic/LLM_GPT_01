from django.db import models
from django.conf import settings


class Chatbot(models.Model):
    user_message = models.TextField()
    ai_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.pk)}번째 대화"
