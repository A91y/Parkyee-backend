from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created, **kwargs):
    if created:
        token, _ = Token.objects.get_or_create(user=instance)
        token.created = timezone.now()
        token.save()
