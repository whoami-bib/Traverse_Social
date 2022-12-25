from django.contrib import admin
from django.urls import path
from .views import tweet_detail_view,tweet_list_view,tweet_create_view,tweet_action_view,tweet_delete_view,tweet_feed_view,commentView,ComentReplyView


'''
BASE ENDPOINT /api/tweets/
'''

urlpatterns = [
    path('',tweet_list_view),
    path('feed/',tweet_feed_view),
    path('create/',tweet_create_view,name='create-tweet'),
    path('action/',tweet_action_view,name="tweet_like"),
    path('<int:tweet_id>/',tweet_detail_view),
    path('<int:tweet_id>/delete',tweet_delete_view),
    path("comments/<int:pk>/",commentView.as_view(), name="comment-view"),
    path("comments/reply/<int:pk>/",ComentReplyView, name="comment-reply"),


]
