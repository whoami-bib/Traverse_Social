from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


# Create your models here.
User = settings.AUTH_USER_MODEL

class FollowerRelation(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    profile     = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user        = models.OneToOneField(User,on_delete=models.CASCADE)
    location    = models.CharField(max_length=200,null=True,blank=True)
    bio         = models.TextField(max_length=300,null=True,blank=True)
    avatar      = models.FileField(default='default.jpg', upload_to='image/profile/avatar')
    cover_image = models.FileField(default='cover.jpg', upload_to='image/profile/cover')
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    followers   = models.ManyToManyField(User,related_name='following',blank=True)

    def __str__(self):
        return self.user
    

def user_did_save(sender,instance,created,*args, **kwargs):
    if created:
        Profile.objects.get_or_create(user = instance)


post_save.connect(user_did_save,sender=User)