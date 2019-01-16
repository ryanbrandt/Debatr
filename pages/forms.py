from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from pages.models import Profile, Tag, Post
import re

''' Forms for pages application '''


# custom user registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # define what model our form works with
    class Meta:
        # our registration form interacts with User instances
        # e.g. form.save saves to User model
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# user update form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    # form interacts with User model
    class Meta:
        model = User
        # form only updates username and email
        fields = ['username', 'email']


# profile update form
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    interests = forms.CharField(required=False)
    tags = forms.CharField(widget= forms.HiddenInput(), required=False)

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'interests']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['bio'].help_text = '1000 characters or less'
        self.fields['interests'].help_text = 'Descending by interest-level, comma-seperated ' \
                                             'or spaced'

    # make profile tags if interests updated
    def taginate(self):
        if 'interests' in self.changed_data:
            # TODO: FIX REGEX TO ACCEPT MORE PATTERNS; ADD CHECK AT END
            interests = re.split(' |,' ,self.cleaned_data['interests'])
            # grab profile instance, clear m2m relations
            instance = self.save(commit=False)
            instance.tags.clear()
            # make new user tags
            for interest in interests:
                interest = interest.lower()
                # see if tag object already exists, no duplicates, else make new tag, add to user
                cur_tag = None
                try:
                    cur_tag = Tag.objects.get(tag__iexact = interest)
                except Tag.DoesNotExist:
                    pass
                if cur_tag:
                    instance.tags.add(cur_tag)
                else:
                    cur_tag = Tag.objects.create(tag=interest)
                    instance.tags.add(cur_tag)

# simple post creation form for user 'feed' posts
class PostCreationForm(forms.Form):
    post = forms.CharField(required=False)
    post_type = forms.ChoiceField(required=False, choices=Post.post_choices)

    class Meta:
        model = Post
        fields = ['post', 'post_type']


    def __init__(self, *args, **kwargs):
        super(PostCreationForm, self).__init__(*args, **kwargs)
        self.fields['post_type'].label = 'Post Type'
        self.fields['post'].help_text = 'Only your followers can view your posts'
        self.fields['post_type'].help_text = 'Optional post category so your followers know what/why your sharing'

    def save(self, user):
        data = self.cleaned_data
        Post.objects.create(content=data['post'], author=user, post_type=data['post_type'])