from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import api_views

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('login/', api_views.login_api, name='api-login'),
    path('register/', api_views.register_api, name='api-register'),
    path('posts', api_views.posts_view, name='posts-views'),
    path('posts/create', api_views.create_posts_view, name='create-posts-views'),
    path('posts/<int:pk>/delete', api_views.delete_posts_view, name='delete-posts-views'),
    path('like/<int:pk>', api_views.like_api, name="like-api"),
    path('comment/<int:pk>', api_views.comment_api, name="comment-api"),

    path('swagger<format>.json|.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]