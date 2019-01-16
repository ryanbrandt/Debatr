from django import forms
from .models import Message, Thread, DebateComment
from messaging import views
from datetime import datetime

''' Forms for messaging application '''


# create new message form
class MessageForm(forms.Form):
    message = forms.CharField(required=False)

    class Meta:
        model = Message
        fields = ['message']

    # saves message if nonempty and valid, updates associated thread timestamp
    def save(self, user, thread):
        data = self.cleaned_data
        message = Message(message=data['message'], user=user, thread=thread)
        # make sure not empty
        if message.message:
            message.save()
            thread.timestamp = datetime.now()
            thread.save()


class DebateCommentForm(forms.Form):
    comment = forms.CharField(required=False)

    class Meta:
        model = DebateComment
        fields = ['comment']

    def save(self, user, thread):
        data = self.cleaned_data
        comment = DebateComment(comment=data['comment'], thread=thread, user=user)

        if comment.comment:
            comment.save()