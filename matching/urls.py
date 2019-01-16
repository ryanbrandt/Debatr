from django.urls import path
from . import views
urlpatterns =[

    path('debate-match/', views.matching, name='matching'),

]