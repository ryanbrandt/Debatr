from django.db import models
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

''' Models for messaging application '''

# TODO: add debate archiving system for closed debates


# thread objects, associates two users to one chat thread and a timestamp
class Thread(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two')
    timestamp = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(null=True, max_length=50)
    accepted = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    # get function to retrieve thread with users or create thread with users if DNE, for async
    def get_or_new(self, user, other_username):
        username = user.username
        if username == other_username:
            return None
        # get other user object, check if thread exists with users
        other_user = User.objects.get(username=other_username)
        try:
           cur_thread = Thread.objects.get(user_one=user, user_two=other_user)

        except Thread.DoesNotExist:
            try:
                cur_thread = Thread.objects.get(user_one=other_user, user_two=user)

                # if no thread, create new one
            except Thread.DoesNotExist:
                cur_thread = Thread(user_one=user, user_two=other_user)
                cur_thread.save()

        return cur_thread


# message objects, associates a user and timestamp to a message in a thread
class Message(models.Model):
    thread = models.ForeignKey(Thread, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class DebateComment(models.Model):
    thread = models.ForeignKey(Thread, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)