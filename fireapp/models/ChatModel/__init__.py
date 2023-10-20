from django.db import models


class ChatModel(models.Model):
    receiver_id = models.IntegerField()
    message = models.TextField()
