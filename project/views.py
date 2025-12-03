import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib import messages
from project.forms.login_forms import LoginForm
from project.forms.register_forms import RegisterForm
from project.forms.post_forms import PostForm
from project.models import *

def index(request):
    if request.user.is_authenticated:
                    posts = Post.objects.annotate(
                liked_by_user=Count('likes', filter=Q(likes__user=request.user, likes__is_like=True))
            ).order_by('-date')
    else:
        posts = Post.objects.all().order_by('-date')
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)   # do NOT save yet
            post.user = request.user         # attach logged-in user
            post.save()
            return redirect("website:index")
        return render(request, 'post/post.html', context={"form": form, 'posts': posts})
    else:
        form = PostForm()
        return render(request, 'post/post.html', context={"form": form, 'posts': posts})

@login_required
def post_delete(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post:
        if post.image and os.path.isfile(post.image.path):
            os.remove(post.image.path)
        
        if post.video and os.path.isfile(post.video.path):
            os.remove(post.video.path)

        post.delete()
        messages.success(request,'Delete is successful')
        return redirect("website:index")
    else:
        messages.error(request, 'This post not found')
        return redirect("website:index")
    
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('website:index')
        messages.error(request, "Wrong Password or Username")
        return render(request, 'auth/login.html', context={"form": form})
    else:
        form = LoginForm()
        return render(request, 'auth/login.html', context={"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('website:index')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('website:login-view')
        else:
            messages.error(request, "Something was Wrong")
            return render(request, 'auth/register.html', context={"form": form})
            
    else:
        form = RegisterForm()
        return render(request, 'auth/register.html', context={"form": form})

@login_required
def profile_view(request):
    posts = Post.objects.filter(user=request.user).annotate(
    liked_by_user=Count(
        'likes',
        filter=Q(likes__user=request.user, likes__is_like=True)
    )
).order_by('-date')
    total_likes = sum(p.likes.count() for p in posts)
    total_comments = sum(p.comments.count() for p in posts)
    return render(request, 'profile/index.html', context={"posts": posts, "total_likes": total_likes, "total_comments": total_comments,})

@login_required
def profile_like_view(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post:
        like=Like.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
        else:
            Like.objects.create(user=request.user, post=post)
            
    if request.headers.get("HX-Request"):
        response = HttpResponse()
        response["HX-Refresh"] = "true"
        return response
    return redirect('website:profile-view')

@login_required
def profile_comment_view(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post:
        Comment.objects.create(post=post, user=request.user, comment= request.POST.get('comment-text'))
    
    if request.headers.get("HX-Request"):
        response = HttpResponse()
        response["HX-Refresh"] = "true"
        return response
    return redirect('website:profile-view')

@login_required
def profile_post_delete(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post:
        if post.image and os.path.isfile(post.image.path):
            os.remove(post.image.path)
        
        if post.video and os.path.isfile(post.video.path):
            os.remove(post.video.path)

        post.delete()
        messages.success(request,'Delete is successful')
        return redirect("website:profile-view")
    else:
        messages.error(request, 'This post not found')
        return redirect("website:profile-view")

@login_required   
def like_view(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post:
        like=Like.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
        else:
            Like.objects.create(user=request.user, post=post)
    if request.headers.get("HX-Request"):
        response = HttpResponse()
        response["HX-Refresh"] = "true"
        return response
    return redirect('website:index')

@login_required
def comment_view(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post:
        Comment.objects.create(post=post, user=request.user, comment= request.POST.get('comment-text'))
    if request.headers.get("HX-Request"):
        response = HttpResponse()
        response["HX-Refresh"] = "true"
        return response
    return redirect('website:index')
    