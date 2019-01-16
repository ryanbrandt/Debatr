from django.contrib import admin
from .models import Thread, Message

''' Message models registered with Django backend CMS '''

admin.site.register(Thread)
admin.site.register(Message)