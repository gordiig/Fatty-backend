from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, **kwargs):
    if not created:
        return
    # Creating Token
    Token.objects.create(user=instance)
