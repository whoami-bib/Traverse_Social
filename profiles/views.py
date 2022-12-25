from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from .models import Profile
from .serializers import PublicProfileSerializer,UpdateUserSerializer

from rest_framework import generics



User = get_user_model()

@api_view(['GET','POST'])
def ProfileDetailView(request,username,*args, **kwargs):
    # This should get the profile of the passed username
    qs = Profile.objects.filter(user__username =username )
    if not qs.exists():
        return Response({"detail":"user not found"},status = 404)
    profile_obj = qs.first()
    data    = request.data or {}
    if request.method == 'POST':
        me        = request.user
        action    = data.get("action")
        if profile_obj.user != me:
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)
            else:
                pass
    serializer = PublicProfileSerializer(instance = profile_obj,context={"request":request})
    return Response(serializer.data,status = 200)

@api_view(['GET','POST'])
def UserProfileUpdate(request,*args, **kwargs):
    user = request.user
    qs = Profile.objects.filter(user = user)
    profile_obj = qs.first()
    serializer = UpdateUserSerializer(instance = profile_obj,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data,{"message":"success"})


