from django.db import models


class LoginModel(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
