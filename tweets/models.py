from django.db import models
from django.conf import settings
from django.db.models import Q


User = settings.AUTH_USER_MODEL

# Create your models here.

class TweetLike(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    tweet        = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp    = models.DateTimeField(auto_now_add=True)



class TweetQuerySet(models.QuerySet):
    def feed(self,user):
        profiles_exist = user.following.exists()
        followed_user_id=[]
        if profiles_exist:
            followed_user_id =user.following.values_list("user__id",flat = True)   # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in= followed_user_id) | 
            Q(user = user)).order_by("-timestamp")


class TweetManager(models.Manager):
    def get_queryset(self,*args, **kwargs):
        return TweetQuerySet(self.model,using=self._db)
    
    def feed(self,user):
        return self.get_queryset().feed(user)


# Model for tweet

class Tweet(models.Model):
    parent       = models.ForeignKey("self",null=True,on_delete=models.SET_NULL)
    user         = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tweets")
    likes        = models.ManyToManyField(User,related_name='tweet_user',blank=True,through=TweetLike)
    content      = models.TextField(blank=True,null=True)
    image        = models.FileField(upload_to='image/tweet', blank=True,null=True)
    timestamp    = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    class Meta:
        ordering = ['-id']
        
    @property
    def is_retweet(self):
        return self.parent != None

# Model for comment 

class Comment(models.Model):
    body        = models.TextField()
    likes       = models.ManyToManyField(User,related_name='comment_likes',blank=True)
    author      = models.ForeignKey(User, related_name="authors", on_delete=models.CASCADE)
    post        = models.ForeignKey(Tweet,related_name="parent_tweet",on_delete=models.CASCADE)
    created     = models.DateTimeField(auto_now_add=True)
    parent      = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,related_name="parentchild")

    def __str__(self):
        return str(self.body[:15])

    @property
    def is_parent(self):
        return True if self.parent is None else False

    @property
    def like_comment(self):
        return self.likes.count()

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created').all()