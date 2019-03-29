from django.contrib import admin
from django.urls import path, re_path
from One.views import music, login, logout, register, username_var

urlpatterns = [
    path('find_music/', music),
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('username_var/', username_var)
]
