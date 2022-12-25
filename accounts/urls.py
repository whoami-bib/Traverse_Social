from .views import RegisterAPI,LoginAPI
from django.urls import path
from knox import views as knox_views


'''
BASE ENDPOINT /api/user/
'''

urlpatterns = [
    
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),

]