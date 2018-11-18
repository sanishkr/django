# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class IGuser(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class mkimg(models.Model):
    ImageURL = models.TextField()
    Xpos = models.FloatField()
    Ypos = models.FloatField()
    Height = models.FloatField()
    Width = models.FloatField()
    Rotation = models.FloatField()

    def __str__(self):
        return  self.ticker