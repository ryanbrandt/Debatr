from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from .models import Notification


# bi-daily task to delete user notification objects that haven't been re-used to optimize notification queries
@periodic_task(run_every=crontab(hour='*48/'))
def delete_dead_notifications():
    try:
        read_notifs = Notification.objects.filter(read=True)
        for notif in read_notifs:
            if (timezone.now()-notif.time).days > 2:
                notif.delete()
    except Notification.DoesNotExist:
        return
