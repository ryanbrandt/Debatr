from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from messaging.models import Message, Thread
from .models import Notification
from datetime import datetime

''' Signals for Notifications '''


# if message received, create notification object
@receiver(signal=post_save, sender=Message)
def make_message_notifcation(sender, instance, created, **kwargs):
    if created:
        thread = instance.thread
        if instance.user == thread.user_one:
            username = thread.user_two
        else:
            username = thread.user_one
        # no duplicate notifications (e.g., only one notification for any n messages from a user)
        try:
            cur_notifications = Notification.objects.filter(user=username)
            exists = False
            for notification in cur_notifications:
                if notification.notification.split()[-1] == instance.user.username:
                    exists = True
                    found_notification = notification
                    break
            if exists:
                found_notification.time = datetime.now()
                found_notification.read = False
                found_notification.save()
            else:
                new_not = Notification.objects.create(notification='New message from ' f'{instance.user.username}', user=username)
        except Notification.DoesNotExist:
            new_not = Notification.objects.create(notification='New message from ' f'{instance.user.username}', user=username)


# if thread created (e.g. thread request sent), create notification object
@receiver(signal=post_save, sender=Thread)
def make_thread_notification(sender, instance, created, **kwargs):
    if created:
        user_requesting = instance.user_one
        user_requested = instance.user_two
        # read notifications garbage collected every 2 days, but just in case users had recent debate, recycle notification
        try:
            cur_notifications = Notification.objects.filter(user=user_requested)
            exists = False
            for notification in cur_notifications:
                if notification.notification == 'New debate request from ' f'{user_requesting.username}':
                    exists = True
                    found_notification = notification
                    break
            if exists:
                found_notification.read = False
                found_notification.time = datetime.now()
                found_notification.save()
            else:
                new_not = Notification.objects.create(notification='New debate request from ' f'{user_requesting.username}', user=user_requested)

        except Notification.DoesNotExist:
            new_not = Notification.objects.create(notification='New debate request from ' f'{user_requesting.username}', user=user_requested)


# if thread declined/retracted, create notification and set original notification read in case retracted
@receiver(signal=pre_delete, sender=Thread)
def make_decline_notification(sender, instance, using, **kwargs):
    user_declined = instance.user_one
    user_declining = instance.user_two
    # same deal, recycle notification, if exists
    try:
        cur_notifications = Notification.objects.filter(user=user_declined)
        exists = False
        for notification in cur_notifications:
            if notification.notification == 'Debate with ' f'{user_declining.username} declined or retracted':
                exists = True
                found_notification = notification
                break
        if exists:
            found_notification.read = False
            found_notification.time = datetime.now()
            found_notification.save()
        else:
            Notification.objects.create(notification='Debate with ' f'{user_declining.username} declined or retracted', user=user_declined)

    except Notification.DoesNotExist:
        # send declined/retracting user a notification
        Notification.objects.create(notification='Debate with ' f'{user_declining.username} declined or retracted', user=user_declined)

    # set requested user's notification read, just in case it was retracted
    orig_not = Notification.objects.get(user=user_declining, notification='New debate request from ' f'{user_declined.username}')
    orig_not.read = True
    orig_not.save()
