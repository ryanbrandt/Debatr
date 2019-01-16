from django.contrib import admin
from django.urls import path
from notifications import views

''' Notifications URLs '''

urlpatterns = [

    path('notifications/?P<username>/', views.notifications_view, name='notifications'),

]