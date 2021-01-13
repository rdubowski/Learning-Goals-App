from django.db.models.signals import post_save
from django.contrib.auth.models import User


from .models import Profile


def profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )
        print('Profile created!')


post_save.connect(profile, sender=User)
