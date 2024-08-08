from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'replies', views.ReplyViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.user_logout, name='api_logout'),
    path('api/register/', views.register_view, name='register_view'),
    path('api/user-status', views.user_status, name='api_user_status'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/categories/', views.list_categories, name='list_categories'),
    path('api/add_post/', views.add_post, name='api_add_post'),
    path('api/user_status/', views.user_status, name='user_status'),
    path('api/protected/', views.protected, name='protected'),
    path('api/add_comment/<int:post_id>/', views.add_comment, name = 'add_comment'),
    path('api/delete_comment/<int:comment_id>/', views.delete_comment, name = 'delete_comment'),
    path('api/add_reply/<int:comment_id>/', views.add_reply, name = 'add_reply'),
    path('api/delete_reply/<int:reply_id>/', views.delete_reply, name = 'delete_reply'),
    path('api/post/<int:post_id>/', views.get_post, name = 'api/get_post'),
    path('api/category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('api/like_comment/<int:comment_id>/', views.like_comment, name = 'like_comment'),
    path('api/dislike_comment/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
    path('api/like_reply/<int:reply_id>/', views.like_reply, name="like_reply"),
    path('api/dislike_reply/<int:reply_id>/', views.dislike_reply, name= "dislike_reply"),
    path('api/random_post/', views.random_post, name='random_post')
]