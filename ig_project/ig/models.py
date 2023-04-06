from django.db import models
from django.contrib.auth.models import AbstractUser
from ig.manager import UserManager
# Create your models here.
class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    username= models.CharField(unique=True, max_length=16)
    bio = models.CharField(max_length=200, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

class Post(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

class PostLike(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE )

    class Meta:
        unique_together = (('post','user'),)


class PostComment(models.Model):
    comment_text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null= False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)


class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
