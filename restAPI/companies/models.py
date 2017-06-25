from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    open = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()
    # owner = models.ForeignKey('auth.User', related_name='stocks', on_delete=models.CASCADE)
    # highlighted = models.TextField()
    # owner = models.ForeignKey(User)


    def __str__(self):
        return  self.ticker