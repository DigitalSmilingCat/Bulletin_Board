from django.db import models
from django.contrib.auth.models import User


class CheckCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)