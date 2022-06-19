from django.db import models
from django.contrib.auth import get_user_model


class Question(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, blank=False)
    question_text = models.CharField(max_length=250, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT, blank=False)
    answer_text = models.CharField(max_length=30, null=True)
    image_url = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
