from rest_framework import serializers
from django.contrib.auth.models import User
from project.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'date']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'is_like','date']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer( many=True, read_only=True)
    likes = LikeSerializer( many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'image', 'video', 'date', 'likes', 'comments')
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_video(self, obj):
        request = self.context.get('request')
        if obj.video:
            return request.build_absolute_uri(obj.video.url) if request else obj.video.url
        return None
    
