from rest_framework import serializers
from .models import Post, Comment, Reply, Category
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')



class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ('id', 'user', 'comment', 'content', 'likes', 'dislikes', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'content', 'likes', 'dislikes', 'replies', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'publish', 'content', 'description', 'author', 'category', 'comments')

class CommentFormSerializer(serializers.Serializer):
    content = serializers.CharField()

class ReplyFormSerializer(serializers.Serializer):
    content = serializers.CharField()

