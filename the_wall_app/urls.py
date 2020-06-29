from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('message', views.create_message),
    path('comment', views.create_comment),
    path('login', views.login),
    path('logout', views.logout),
]
