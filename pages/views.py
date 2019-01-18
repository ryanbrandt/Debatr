from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from pages.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from pages.models import User, Profile, Post
from messaging.models import Thread
from datetime import datetime
from datetime import timedelta
from django.core import serializers
from django.http import HttpResponse
import json

''' Views for simple webpages application '''


# homepage view
# TODO: post like system? post replies? see more posts? global post feed, integrate post images into front end
def home(request):
    form = None
    recent_feed = None

    if request.user.is_authenticated:
        user = request.user
        form = PostCreationForm()
        recent_feed = Post.objects.filter(Q(author__in=user.profile.following.all()) | Q(author=user)).order_by('-date_posted')[:30]

    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        post_type = request.POST.get('type')

        if form.is_valid():
            form.save(user, post_type)

    # ajax if user submits new post or every 15 seconds, fetch unseen posts pass to js
    if request.is_ajax():
        last_time = datetime.now() - timedelta(seconds=15)
        new_posts = Post.objects.filter(date_posted__gt=last_time)

        # not best way to do this, should be scalable since frequent, would have to revisit for large user base
        new_posts = serializers.serialize('json', new_posts)
        new_posts = json.loads(new_posts)
        for post in new_posts:
            cur_id = int(post['fields']['author'])
            post['fields']['username'] = User.objects.get(id=cur_id).username
            post['fields']['image'] = User.objects.get(id=cur_id).profile.image.url

        new_posts = json.dumps(new_posts)
        return HttpResponse(new_posts, content_type='application/json')

    return render(request, "home.html", {'form': form, 'recent_feed': recent_feed})


@login_required
def getting_started(request):
    return render(request, 'getting_started.html', {})


# about-us view
def aboutus(request):
    return render(request, "aboutus.html", {})


# user login view
def login(request):
    return render(request, "login.html", {})


# user registration view
def join(request):
    # if register form sent, grab
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # if valid form, send success message and send to login
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully created for {username}! Sign in below')
            # save user
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "join.html", {'form': form})


@login_required
# user personal profile view
def profile(request, username=None):
    # if user gets link to another users profile (e.g. my-profile/...) bring them to correct view
    if username != request.user.username:
        return redirect('other-profile', username)

    follower_count = Profile.objects.filter(following=request.user).count()
    following_count = request.user.profile.following.count()
    return render(request, "user_profile.html", {'follower_count': follower_count, 'following_count': following_count})


# user update profile view
@login_required
def update_profile(request):
    # if updates submitted, grab
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # profile has image field so also get files
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # check updates valid, save and 'taginate'
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Successfully Updated!')
            profile_form.taginate()
            return redirect('profile',  username=request.user.username)
    else:
        # instance populates forms with current information
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "update_profile.html", {'user_form': user_form, 'profile_form': profile_form})


# TODO: page with twitter AI bot feed on political/social topics
def trending(request):
    return render(request, "trending.html", {})


# TODO: make some sort of blog thing?
@login_required
def consideration(request):
    return render(request, "consideration.html", {})


# user search view
@login_required
def search(request, username=None):
    # if user selects a view profile, username gets defined, pass to other_profile view
    if username:
        return other_profile(request, username)
    else:
        # query db for variable q entered in search
        query = request.GET.get('q')
        user_results = User.objects.filter(Q(username__icontains=query))
        # filter out current user
        user_results = user_results.exclude(username=request.user.username)
        # get related debates
        thread_results = Thread.objects.filter(Q(topic__icontains=query))
        # filter any of user's debates and any un-accepted debates
        thread_results = thread_results.exclude(Q(user_one=request.user) | Q(user_two=request.user))
        thread_results = thread_results.exclude(Q(accepted=False))
    return render(request, "search.html", {'results': user_results, 'query': query, 'thread_results': thread_results})


# other profile view (e.g. view for profiles that aren't current users)
@login_required
def other_profile(request, username):
        # get user with username selected from search, need fields to populate template
        user_visiting = User.objects.get(username=username)
        # send to profile view if owner of profile
        if request.user == user_visiting:
            return redirect('profile', username=username)
        # send to template as user_visiting so user (logged in user) isn't overwritten and navBar functions correctly
        if request.is_ajax():
            cur_user = request.user
            if user_visiting not in cur_user.profile.following.all():
                cur_user.profile.following.add(user_visiting)
                messages.success(request, f'{user_visiting.username} successfully followed!')
            else:
                cur_user.profile.following.remove(user_visiting)
                messages.success(request, f'{user_visiting.username} successfully unfollowed!')

        return render(request, "other_profile.html", {'user_visiting': user_visiting})

