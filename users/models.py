from __future__ import unicode_literals
#
from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):
    follower = models.ForeignKey(User, related_name="followees",on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name="followers",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)