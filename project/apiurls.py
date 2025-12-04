from django.urls import path
from . import api_views
urlpatterns = [
    path('login/', api_views.login_api, name='api-login'),
    path('register/', api_views.register_api, name='api-register'),
    path('posts', api_views.posts_view, name='posts-views'),
    path('posts/create', api_views.create_posts_view, name='create-posts-views'),
    path('posts/<int:pk>/delete', api_views.delete_posts_view, name='delete-posts-views'),
    path('posts/<int:pk>/edit', api_views.edit_posts_view, name='edit-posts-views'),
    path('like/<int:pk>', api_views.like_api, name="like-api"),
    path('comment/<int:pk>', api_views.comment_api, name="comment-api"),
]