from django.urls import path, include
from . import views

app_name = "website"
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/delete', views.post_delete, name='post-delete'),
    path('login/', views.login_view, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
    path('regiter/', views.register_view, name='register-view'),
    path('profile/', views.profile_view, name="profile-view"),
    path('profile/like/<int:pk>', views.profile_like_view, name="profile-like-view"),
    path('profile/comment/<int:pk>', views.profile_comment_view, name="profile-comment-view"),
    path('profile/post/<int:pk>/delete', views.profile_post_delete, name='profile-post-delete'),
    path('like/<int:pk>', views.like_view, name="like-view"),
    path('comment/<int:pk>', views.comment_view, name="comment-view"),
]