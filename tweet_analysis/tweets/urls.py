from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('export/', views.export_tweets, name='export_tweets'),
    path('graphs/', views.graphs, name='graphs'),
]