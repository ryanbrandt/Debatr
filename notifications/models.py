from django.db import models
from django.contrib.auth.models import User

''' Notifications Models '''


# TODO: adjust model for friend notifcations/comment notifications when implemented
# notification objects, associated with a user
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=80)
    read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)