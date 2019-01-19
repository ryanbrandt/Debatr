from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MessageForm, DebateCommentForm
from .models import Thread, Message, DebateComment
from notifications.models import Notification
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core import serializers
from django.http import HttpResponse

''' Views for messaging application '''

# TODO: (DONE 01/18) fix retract & accept so they set directing notification to read


# inbox view
@login_required
def messaging(request, username):
    # obviously, logged in user can only visit their inbox
    user = request.user
    if username != user.username:
        messages.warning(request, f'{user.username} you are not authorized to view this page!')
        return redirect('home')
    else:
        # query db, get threads associated with user, sort by recent
        threads = Thread.objects.filter((Q(user_one = user) | Q(user_two = user)) & Q(closed=False)).order_by('-timestamp')
        recent_msgs = []
        # TODO
        for thread in threads:
            try:
                 recent_msgs.append(Message.objects.filter(Q(thread=thread)).order_by('-timestamp').first())
            except Message.DoesNotExist:
                 recent_msgs.append(None)

    return render(request, "inbox.html", {'threads': threads, 'recent': recent_msgs})


# individual thread view
@login_required
def thread(request, username):
    # get user, chat partner
    partner = User.objects.get(username=username)
    user = request.user
    # not most efficient way to go about this, but see if user redirected here from notifications, set notification read
    try:
        notif = 'New message from ' f'{partner.username}'
        notif_obj = Notification.objects.get(user=user, notification=notif, read=False)
        notif_obj.read = True
        notif_obj.save()
    except Notification.DoesNotExist:
        try:
            notif = 'New debate request from ' f'{partner.username}'
            notif_obj = Notification.objects.get(user=user, notification=notif)
            notif_obj.read = True
            notif_obj.save()
        except Notification.DoesNotExist:
            pass

    # retrieve thread if exists; if DNE, redirect to new thread view to make thread
    try:
        cur_thread = Thread.objects.get(user_one=user, user_two=partner, closed=False)

    except Thread.DoesNotExist:
        try:
            cur_thread = Thread.objects.get(user_one=partner, user_two=user, closed=False)

        except Thread.DoesNotExist:
            return redirect('new_thread', username=partner.username)
    # get message, if one, save it to thread
    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            form.save(user=user, thread=cur_thread)
    # retrieve all messages from thread to unload in template
    thread_messages = Message.objects.filter(Q(thread=cur_thread)).order_by('timestamp')
    form = MessageForm()
    return render(request, 'thread.html', {'form': form, 'thread_messages': thread_messages, 'partner': partner, 'thread': cur_thread})


# view for new debate request page
@login_required
def new_thread(request, username):

    if request.method == 'POST':
        topic = request.POST.get('message')
        new_thread = Thread.objects.create(user_one=request.user, user_two=User.objects.get(username=username), topic=topic)
        messages.success(request, f'Debate on {topic} request successfully sent to {username}!')
        return redirect('thread', username=username)

    form = MessageForm()
    msg = form.__dict__["fields"]["message"]
    msg.label = 'Your Topic'
    msg.required = True
    msg.help_text = '50 characters or less, topics should be concise and clear'
    msg.max_length = 50
    return render(request, 'new_thread.html', {'partner': username, 'form': form})


# decline or retract debate request view, deletes thread immediately
@login_required
def retract_or_decline(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    user_one = thread.user_one
    user_two = thread.user_two
    thread.delete()
    # set request notifcation to read, don't know if requester or requested denied so double try
    try:
        notif = 'New debate request from ' f'{user_one.username}'
        notif_obj = Notification.objects.get(user=user_two, notification=notif)
        notif_obj.read = True
        notif_obj.save()
    except Notification.DoesNotExist:
        try:
            notif = 'New debate request from ' f'{user_two.username}'
            notif_obj = Notification.objects.get(user=user_one, notification=notif)
            notif_obj.read = True
            notif_obj.save()
        except Notification.DoesNotExist:
            pass

    return render(request, 'decline.html', {'one': user_one, 'two': user_two})


# accept view, just redirects to thread, just need buffer to set thread to accepted
@login_required
def accept(request, username):
    partner = User.objects.get(username=username)
    user = request.user
    thread_accepted = Thread.objects.get(user_one=partner, user_two=user, closed=False)
    thread_accepted.accepted = True
    thread_accepted.save()
    messages.success(request, f'Debate on {thread_accepted.topic} with {partner.username} accepted! Get started below')
    # set request notification to read
    try:
        notif = 'New debate request from ' f'{partner.username}'
        notif_obj = Notification.objects.get(user=user, notification=notif)
        notif_obj.read = True
        notif_obj.save()
    except Notification.DoesNotExist:
        pass

    return redirect('thread', username=username)


# spectate view
# TODO: add ajax for periodic comment fetching
@login_required
def spectate(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    user = request.user

    if thread.closed:
        messages.warning(request, 'This debate has concluded')

    # FIXME: safety, see if we can get rid off
    if user == thread.user_one and not thread.closed:
        return redirect('thread', username=thread.user_two.username)
    if user == thread.user_two and not thread.closed:
        return redirect('thread', username=thread.user_one.username)

    if request.method == 'POST':
        form = DebateCommentForm(request.POST)

        if form.is_valid():
            form.save(user=user, thread=thread)
            return redirect('spectate', thread_id=thread_id)

    thread_messages = Message.objects.filter(thread=thread)
    comments = DebateComment.objects.filter(thread=thread)
    form = DebateCommentForm()
    cmnt = form.__dict__["fields"]["comment"]
    cmnt.help_text = '500 character maximum, comments are only visible to other spectators until the debate has concluded'

    # if ajax timer goes off, fetch messages from last 15 seconds, if any, and send to js to update DOM
    if request.is_ajax():
        last_time = datetime.now() - timedelta(seconds=15)
        new_messages_list = Message.objects.filter(thread=thread, timestamp__gt=last_time)
        new_messages_list = serializers.serialize("json", new_messages_list)
        return HttpResponse(new_messages_list, content_type='application/json')

    return render(request, 'spectate.html', {'thread': thread, 'thread_messages': thread_messages, 'form': form, 'comments': comments})


@login_required
def follow_thread(request, thread_id):
   user = request.user
   user.profile.threads.add(Thread.objects.get(id=thread_id))
   messages.success(request, 'You are now following this debate! You can view it from your Debate Feed')
   return spectate(request, thread_id)


@login_required
def unfollow_thread(request, thread_id):
    user = request.user
    user.profile.threads.remove(Thread.objects.get(id=thread_id))
    messages.success(request, 'You have successfully unfollowed this debate! It is removed from your Debate Feed')
    return spectate(request, thread_id)


# TODO: add ajax for unfollowing debates like unfollowing users works
@login_required
def debate_feed(request, username):
    user = request.user
    followed_threads = user.profile.threads.all()
    return render(request, 'debatefeed.html', {'threads': followed_threads})


@login_required
def close_thread(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    thread.closed = True
    thread.save()
    return redirect('spectate', thread_id=thread_id)