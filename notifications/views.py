from rest_framework import viewsets, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from tweets.pagination import CustomPagination

User = get_user_model()


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def NotificationView(request):
    notify_list = Notification.objects.filter(
        to_user=request.user,
    ).order_by('-id')
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(notify_list,request)
    noti_count = Notification.objects.filter(
        to_user=request.user,
        user_has_seen=False
    ).count()
    """
    If there is no messages then we will not show notification tag
    we just send null value to notification count from server if count is 0
    """
    if noti_count == 0:
        noti_count  = None  
    serializer = NotificationSerializer(result_page, many=True, context={
                                        
                                        'request': request
                                        })
    # return Response(serializer.data)
    return paginator.get_paginated_response({'data':serializer.data,'noti_count': noti_count})
    
class NotificationSeen(APIView):
    def get(self, request):
        notify_list = Notification.objects.filter(
            to_user=request.user,
            user_has_seen=False
        )
        for i in notify_list:
            i.user_has_seen = True
            i.save()
        Notification.objects.filter(
            Q(notification_type='M',
              to_user=request.user,
              ) 
        ).delete()
        return Response({"user_seen": True})
    
    def post(self,request):
        data = request.data
        notification = get_object_or_404(Notification,id=data.get('notify_id'))
        if notification.to_user == request.user:
            notification.user_has_seen =  True
            notification.delete()
            return Response({"notification_deleted": True})