from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from pages.models import Profile, Post
from messaging.models import Thread
from notifications.models import Notification
from django.contrib import messages

''' Signals for pages application '''


# if user created, make user an associated profile
@receiver(signal=post_save, sender=User)
def make_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# save associated profile whenever user saved
@receiver(signal=post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# if new thread accepted, make user post for both users involved so followers can see and spectate
@receiver(signal=pre_save, sender=Thread)
def make_debate_post(sender, instance, **kwargs):
    if instance.accepted:
        Post.objects.create(author=instance.user_one, content=f'New debate with {instance.user_two} on {instance.topic} accepted!', post_type='ND', post_thread=instance)
        Post.objects.create(author=instance.user_two, content=f'New debate with {instance.user_one} on {instance.topic} accepted!', post_type='ND', post_thread=instance)
