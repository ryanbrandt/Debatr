from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from messaging.models import Thread
from PIL import Image

''' Models for General Webpages '''

# TODO: add 'followed debates' to profiles


# model for tagging system
class Tag(models.Model):
    tag = models.CharField(max_length=18)


# post model for users/staff to add to For Your Consideration
class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # if user deleted, so are posts
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_choices = (
        ('','--'),
        ('LFD', 'Looking for a debate'),
        ('FYC', 'For your consideration'),
        ('SI', 'Seeking information'),
        ('ND', 'New Debate'),
    )
    post_type = models.CharField(max_length=1, choices=post_choices)
    post_image = models.ImageField(default=None, null=True)
    post_thread = models.ForeignKey(Thread, default=None, null=True, on_delete=models.CASCADE)


# user profile model
class Profile(models.Model):
    # associate user with Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user picture
    image = models.ImageField(default='default.jpg')
    bio = models.CharField(null=True,max_length=500)
    interests = models.CharField(null=True, max_length=40)
    tags = models.ManyToManyField(Tag)
    threads = models.ManyToManyField(Thread)
    following = models.ManyToManyField(User, related_name='following')

    # toString
    def __str__(self):
        return f'{self.user.username} Profile'

    # override save to resize images to 300x300
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # get image user saving
        img = Image.open(self.image.path)
        # if greater than 300x300, resize and save
        if img.width > 300 or img.height > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


