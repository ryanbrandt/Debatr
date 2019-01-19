from django.urls import path
from . import views

''' URLs for messaging application '''

urlpatterns = [
    path('my-inbox/?P<username>/', views.messaging, name='inbox'),
    path('messaging/?P<username>/', views.thread, name='thread'),
    path('start-debate/?P<username>/', views.new_thread, name='new_thread'),
    path('debate-declined/?P<thread_id>/', views.retract_or_decline, name='decline'),
    path('debate-accepted/?P<username>/', views.accept, name='accept'),
    path('spectate/?P<thread_id>/', views.spectate, name='spectate'),
    path('follow-debate/?P<thread_id>/', views.follow_thread, name='follow_thread'),
    path('unfollow-debate/?P<thread_id>/', views.unfollow_thread, name='unfollow_thread'),
    path('debate-feed/?P<username>/', views.debate_feed, name='debatefeed'),
    path('close-debate/?P<thread_id>/', views.close_thread, name='close_thread'),
]