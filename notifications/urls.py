from django.urls import path
from .import views

'''
BASE ENDPOINT /api/notification/
'''

urlpatterns = [
    path('notification_list/', views.NotificationView, name="notification-list"),
    path('notification_seen_delete/',
         views.NotificationSeen.as_view(), name="notification-seen"),
]