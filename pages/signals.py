from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from pages.models import Profile

''' Signals for pages application (more specifically, user model) '''


# if user created, make user an associated profile
@receiver(signal=post_save, sender=User)
def make_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# save associated profile whenever user saved
@receiver(signal=post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

