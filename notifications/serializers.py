from .models import Notification
from rest_framework import serializers
from accounts.serializers import RegisterSerializer

class NotificationSerializer(serializers.ModelSerializer):
    from_user = RegisterSerializer(read_only=True)
    to_user = serializers.StringRelatedField(read_only=True)
    noti_count = serializers.SerializerMethodField(read_only=True)
    # tweet = AnonTweetSerializer(read_only=True)
    # comment = LessCommentSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'
    
    def get_noti_count(self,obj):
        count = self.context.get('noti_count')
        return count