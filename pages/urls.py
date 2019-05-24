from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

''' URLs for pages application '''

urlpatterns = [
    path('', views.home, name = 'home'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'home.html'), name = 'logout'),
    path('about-us/', views.aboutus, name = 'aboutus'),
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('join-debatr/', views.join, name = 'join'),
    path('my-profile/?P<username>/', views.profile, name = 'profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('trending-issues/', views.trending, name = 'trending'),
    path('search/', views.search, name = 'search'),
    path('for-your-consideration/', views.consideration, name = 'consideration'),
    path('user-profile/?P<username>/', views.other_profile, name = 'other-profile'),
    path('getting-started/', views.getting_started, name='getting-started'),
    path('notifications-ajax/', views.get_notifications, name='notification-ajax'),
    path('comments-ajax/', views.get_comments, name='comments-ajax'),
]