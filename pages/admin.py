from django.contrib import admin
from pages.models import Post, Profile, Tag

''' Pages models registered with Django backend CMS '''

# register models to be handled in admin page
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Tag)
