from rest_framework import serializers
from django.conf import settings

from .models import Tweet,Comment
from profiles.serializers import PublicProfileSerializer

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
MIN_TWEET_LENGTH = 5
TWEET_ACTION_OPTIONS  = ["like","unlike","retweet"]

class TweetActionSerializer(serializers.Serializer):
    id      =   serializers.IntegerField()
    action  =   serializers.CharField()
    content  =   serializers.CharField(allow_blank = True,required = False)

    def validate_action(self,value):
        value = value.lower()
        if not TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is action is not valid")
        return value



class TweetCreateSerializer(serializers.ModelSerializer):
    user     =  PublicProfileSerializer(source='user.profile',read_only = True) #serializers.SerializerMethodField(read_only = True)
    likes    =  serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ["user","id","content","likes","image"]
    def get_likes(self,obj):
        return obj.likes.count()

    def validate_content(self,value):
        # content = self.cleaned_data.get("content")
        if len(value) > MAX_TWEET_LENGTH  and len(value) < MIN_TWEET_LENGTH:
            raise serializers.ValidationError("This Traverse is not valid")
        return value
    
    # def get_user(self,obj):
    #     return obj.user.id

class TweetSerializer(serializers.ModelSerializer):
    user     =  PublicProfileSerializer(source='user.profile',read_only = True)
    likes    =  serializers.SerializerMethodField(read_only=True)
    parent   =  TweetCreateSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ["user",
        "id",
        "content",
        "likes",
        "is_retweet",
        "image",
        "parent",
        "user",
        "timestamp"]
    def get_likes(self,obj):
        return obj.likes.count()



# comment serializer


class CommentSerializer(serializers.ModelSerializer):
    # author = PublicProfileSerializer(source='user.profile',read_only = True)
    is_parent = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)
    parentId= serializers.SerializerMethodField(read_only=True)
    
# 'iliked','like_count'

    class Meta:
        model = Comment
        fields = [
            'id','body','author',
            'children','is_parent',
            'parentId','created',
            ]
    def get_iliked(self,obj):
        return True if self.context.get('request').user in obj.likes.all() else False
        
    def get_is_parent(self,obj):
        return obj.is_parent 

    def get_parentId(self,obj):
        if obj.parent:
            return obj.parent.id
        return None

    def get_children(self,obj):
        serializer = CommentSerializer(obj.children, many=True,
        context={'request':self.context.get('request')})
        return serializer.data
    
    # def get_like_count(self,obj):
    #     return obj.likes.count()

    

