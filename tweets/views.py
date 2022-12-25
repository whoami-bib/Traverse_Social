from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.conf import settings
from rest_framework.pagination import PageNumberPagination

from .models import Tweet,Comment

from .serializers import TweetSerializer,TweetActionSerializer,TweetCreateSerializer,CommentSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from .pagination import CustomPagination

from rest_framework import  exceptions
from rest_framework.status import HTTP_201_CREATED
from django.shortcuts import get_object_or_404


# Create your views here.

def home_view(request,*args, **kwargs):
    return render(request,"pages/home.html")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def tweet_create_view(request,*args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        serializer.save(user = request.user)
        return Response(serializer.data,status=201)
    return Response({},status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def tweet_list_view(request,*args, **kwargs):
    print(request.user)
    username = request.user
    print(username)
    if username != None:
        qs = Tweet.objects.filter(user__username__iexact = username)
        print(qs)
    serializer = TweetSerializer(qs,many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def tweet_feed_view(request,*args, **kwargs):
    paginator           = PageNumberPagination()
    paginator.page_size = 20
    user                = request.user
    qs                  = Tweet.objects.feed(user)
    paginated_qs        = paginator.paginate_queryset(qs,request)
    serializer          = TweetSerializer(paginated_qs,many = True)
    return paginator.get_paginated_response(serializer.data)#Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def tweet_detail_view(request,tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj= qs.get(id=tweet_id)
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def tweet_delete_view(request,tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    qs = qs.filter(user =  request.user)
    if not qs.exists():
        return Response({"message":"you cannot delete this traverse"},status = 400)
    obj = qs.first()
    obj.delete()
    return Response({"message":"Traverse removed"},status = 200)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def tweet_action_view(request,*args, **kwargs):
    '''
    id is required
    Actions : Like,Unlike,Retweet.
    '''
    serializer      = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception = True):
        data        =   serializer.validated_data
        tweet_id    =   data.get("id")
        action      =   data.get("action")
        content     =   data.get("content")
        
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({},status=404)
        obj = qs.first()
        if action      == "like":
            obj.likes.add(request.user)
            serializer  = TweetSerializer(obj)
            return Response(serializer.data,status = 200)
        elif action     == "unlike":
            obj.likes.remove(request.user)
            serializer  = TweetSerializer(obj)
            return Response(serializer.data,status = 200)
        elif action     == "retweet":
            new_tweet   =  Tweet.objects.create(user = request.user,parent = obj,content = content)
            serializer  = TweetSerializer(new_tweet)
            return Response(serializer.data,status = 200)
        #this is todo
        return Response({"message":"Traverse removed Successfully"},status = 200)

class commentView(APIView):
    def get_object(self,pk):
        tweet = Tweet.objects.get(id=pk)
        return tweet

    def get(self, request,pk):
        tweet = self.get_object(pk)
        comments = Comment.objects.filter(
            post=tweet, parent=None).order_by('-created')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(comments,request)
        serializer = CommentSerializer(
            result_page, many=True, context={'request': request})
        # return Response(serializer.data)
        return paginator.get_paginated_response(serializer.data)

    def post(self,request,pk):
        data = request.data
        tweet = self.get_object(pk)
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        new_comment = Comment(author=request.user,body=data.get(
            'body'), post=tweet)
        print(new_comment.author.id)
        new_comment.save()

        serializer = CommentSerializer(
            new_comment, context={'request': request})
        return Response(serializer.data,status=HTTP_201_CREATED)


# view for replaying a comment


@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def ComentReplyView(request, pk):
    data = request.data
    if request.method == 'POST':
        tweet = Tweet.objects.get(id=pk)
        parentComId = data.get('comId')
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        parent = Comment.objects.get(id=parentComId)
        new_comment = Comment(parent=parent, body=data.get(
            'body'), author=request.user, post=tweet)
        new_comment.save()
        serializer = CommentSerializer(
            new_comment, context={'request': request})
        return Response(serializer.data,status=HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def like_unlike_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.liked.all():
            liked = False
            comment.liked.remove(request.user)
        else:
            liked = True
            comment.liked.add(request.user)
        return Response({
            'liked': liked,
            'count': comment.like_comment
        })

