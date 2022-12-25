from rest_framework import serializers
from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
    first_name      = serializers.SerializerMethodField(read_only = True)
    last_name       = serializers.SerializerMethodField(read_only = True)
    username        = serializers.SerializerMethodField(read_only = True)
    is_following    = serializers.SerializerMethodField(read_only = True)
    follower_count  = serializers.SerializerMethodField(read_only = True)
    following_count = serializers.SerializerMethodField(read_only = True)
    class Meta:
        

        model = Profile
        fields = [
            'first_name',
            'last_name',
            'id',
            'location',
            'bio',
            'follower_count',
            "following_count",
            'is_following',
            'username'
        ]

    def get_is_following(self,obj):
        is_following    = False
        context         = self.context
        request         = context.get("request")
        if request:
            user         = request.user
            is_following = user in obj.followers.all()
        return is_following

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.first_name

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_follower_count(self, obj):
        return obj.followers.count() 


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name      = serializers.SerializerMethodField()
    last_name       = serializers.SerializerMethodField()
    username        = serializers.SerializerMethodField(read_only = True)
    # is_following    = serializers.SerializerMethodField(read_only = True)
    follower_count  = serializers.SerializerMethodField(read_only = True)
    following_count = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name','location',
            'bio',
            'follower_count',
            "following_count",
            'avatar',
            'username')

    # def validate_email(self, value):
    #     user = self.context['request'].user
    #     if user.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value

    # def validate_username(self, value):
    #     user = self.context['request'].user
    #     if user.objects.exclude(pk=user.pk).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})
    #     return value

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.first_name

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_follower_count(self, obj):
        return obj.followers.count()
