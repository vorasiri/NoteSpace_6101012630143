from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('<int:note_index>/', views.detail,name='detail'),
    path('delete/<int:note_id>/', views.delete, name='delete'),
]
