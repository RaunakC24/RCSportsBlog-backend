from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment, Reply, Category
from .forms import CommentForm, ReplyForm, UserRegisterForm, PostForm
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, CommentSerializer, ReplySerializer, CategorySerializer, CommentFormSerializer, ReplyFormSerializer
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
import random
# Create your views here.

@api_view(['GET'])
def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    post_serializer = PostSerializer(post)

    comment_serializer = CommentSerializer(comments, many=True)
    comment_form_serializer = CommentFormSerializer()
    reply_form_serializer = ReplyFormSerializer()

    data = {
        'post': post_serializer.data,
        'comments': comment_serializer.data,
        'comment_form': comment_form_serializer.data,
        'reply_form':  reply_form_serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        category_id = data.get('category')
        description = data.get('description')
        category = get_object_or_404(Category, id=category_id)
        post = Post.objects.create(title=title, content=content, description=description, category=category, author=request.user)
        return JsonResponse({'message': 'Post created', 'post': PostSerializer(post).data}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    data = json.loads(request.body)
    form = CommentForm(data)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        return JsonResponse({
            'status': 'success',
            'comment': CommentSerializer(comment).data
        }, status=201)
    return JsonResponse({
        'error': 'There was an error',
        'errors': form.errors
    }, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        post_id = comment.post.id
        comment.delete()
        return JsonResponse({'status': 'Success', 'post_id': post_id}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    data = json.loads(request.body)
    form = ReplyForm(data)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.comment = comment
        reply.save()
        return JsonResponse({
            'status': 'success',
            'reply': ReplySerializer(reply).data
        }, status=200)
    return JsonResponse({
        'status': 'There was an error',
        'errors': form.errors
    }, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])    
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id = reply_id)
    post_id = reply.comment.post.id
    reply.delete()
    return JsonResponse({'status': 'Success', 'comment_id': post_id}, status=200)
    
@api_view(['GET'])
def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    serializer = PostSerializer(posts, many=True)
    return Response({'category': CategorySerializer(category).data, 'posts': serializer.data})

@csrf_exempt
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories, 'user': request.user, 'is_authenticated': request.user.is_authenticated})

@csrf_exempt
def user_logout(request):
    logout(request)
    response = JsonResponse({'message': 'Logged out successfully'})
    response.delete_cookie('accessToken')
    response.delete_cookie('refreshToken')
    return response


def check_like_dislike (user, content_type, object_id, is_Like):
    if content_type == 'comment':
        content_object = get_object_or_404(Comment, id=object_id)
    else:
        content_object = get_object_or_404(Reply, id=object_id)
    
    if is_Like:
        if user in content_object.likes.all():
            content_object.likes.remove(user)
            message = 'Like removed'
        else:
            content_object.likes.add(user)
            content_object.dislikes.remove(user)
            message = 'Liked'
    else:
        if user in content_object.dislikes.all():
            content_object.dislikes.remove(user)
            message = 'Dislike removed'
        else:
            content_object.dislikes.add(user)
            content_object.likes.remove(user)
            message = 'Disliked'
    content_object.save()

    return {
        'status': 'success',
        'message': message,
        'likes_count': content_object.likes.count(),
        'dislikes_count': content_object.dislikes.count()
    }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    result = check_like_dislike(request.user, 'comment', comment_id, True)
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_comment(request, comment_id):
    result = check_like_dislike(request.user, 'comment', comment_id, False)
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_reply(request, reply_id):
    result = check_like_dislike(request.user, 'reply', reply_id, True)
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_reply(request, reply_id):
    result = check_like_dislike(request.user, 'reply', reply_id, False)
    return Response(result)


@csrf_exempt
def login_view(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({
                'message': 'Logged in successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'is_superuser': user.is_superuser
            })
            response.set_cookie('accessToken', str(refresh.access_token), httponly=True)
            response.set_cookie('refreshToken', str(refresh), httponly=True)
            response.set_cookie('username', user.username, httponly=True)
            response.set_cookie('is_superuser', user.is_superuser, httponly=True)
            return response
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'message': 'Login required'}, status=400)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username is already taken'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already taken'}, status = 400)
        user = User.objects.create_user(username=username, password=password, email=email)
        refresh = RefreshToken.for_user(user)
        response = JsonResponse({'message': 'User registered', 'user': user.username, 'access': str(refresh.access_token), 'refresh': str(refresh)})
        response.set_cookie('accessToken', str(refresh.access_token), httponly=True)
        response.set_cookie('refreshToken', str(refresh), httponly=True)
        response.set_cookie('username', user.username, httponly=True)
        return response
    return JsonResponse({'message': 'An error occured'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def random_post(request):
    posts = list(Post.objects.all())
    if posts: 
        post = random.choice(posts)
        data = {
            'title': post.title,
            'description': post.description,
            'link': f"/post/{post.id}"
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'No Posts are found'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_status(request):
    return Response({'is_authenticated': True, 'username': request.user.username})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected(request):
    return Response({"message": "This means you are authenticated"})
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer