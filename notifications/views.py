from django.shortcuts import render
from .models import Notification
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.query import Q
from django.contrib.auth.decorators import login_required
import json

''' View for notifications '''


@login_required
def notifications_view(request, username, notification=None):
    # obviously user can only view their notifications
    user = request.user
    if user.username != username:
        messages.warning(request, f'{user.username} you are not authorized to view this page!')
        return redirect('home')

    # ajax to remove notifications on user acknowledge, see template for inline script; here we just set read
    if request.method == 'POST':
        notif = request.POST.get('notification')
        print(notif)
        to_acknowledge = Notification.objects.get(user=user, notification=notif)
        to_acknowledge.read=True
        to_acknowledge.save()

    # querying and avoiding writing a custom template for iterables :)
    notifications = Notification.objects.filter(Q(user_id=user.id)).order_by('-time')
    fixed_notifications = []
    others_involved = []
    times = []
    read = []
    for notification in notifications:
        if notification.notification.split()[0] != 'Debate':
            others_involved.append(notification.notification.split()[-1])
        else:
            others_involved.append(notification.notification)
        fixed_notifications.append(notification.notification)
        times.append(notification.time)
        read.append(notification.read)

    notifications = zip(fixed_notifications, times, others_involved, read)
    return render(request, 'notifications.html', {'notifications': notifications})
