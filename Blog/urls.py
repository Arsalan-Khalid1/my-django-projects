from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('postComments/', views.postComments, name='postComments'),
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),
]
