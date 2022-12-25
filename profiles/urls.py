from django.urls import path
from .views import ProfileDetailView,UserProfileUpdate #EditProfileView

'''
BASE ENDPOINT /api/profiles/
'''

urlpatterns = [
    path('<str:username>/',ProfileDetailView),
    path('<str:username>/follow',ProfileDetailView),
    path('update_profile/my-profile/', UserProfileUpdate, name='auth_update_profile'),
    
]
