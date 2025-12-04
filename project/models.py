from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Info"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post/images', blank=True, null=True)
    video = models.FileField(upload_to='post/videos', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    @property
    def post_get_likes(self):
        return self.likes.filter(is_like=True)
    
    def liked_by_user(self, user):
        return self.likes.filter(user=user, is_like=True).exists()
    
    @property
    def post_get_comments(self):
        return self.comments.all().order_by('-date')
    
    def __str__(self):
        return self.description

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content= models.TextField()
    date = models.DateTimeField(auto_now=True)