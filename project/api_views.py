from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from project.serializers import *
from project.forms.register_forms import RegisterForm
from project.forms.post_forms import PostForm

@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register_api(request):
    form = RegisterForm(request.POST, request.FILES)
    
    if form.is_valid():
        obj = form.save()
        profile_url = None
        if hasattr(obj, 'info') and obj.info and obj.info.profile:
            profile_url = request.build_absolute_uri(obj.info.profile.url)
        
        return JsonResponse({
            "status": status.HTTP_201_CREATED,
            "id": obj.id,
            "username": obj.username,
            "email": obj.email,
            "profile": profile_url,
            "message": "Create is success"
        }, status=status.HTTP_201_CREATED)
    
    else:
        errors = {field: " ".join([str(e) for e in errs]) for field, errs in form.errors.items()}
        return JsonResponse({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def posts_view(request):
    posts = Post.objects.all().order_by('-date')
    serializer = PostSerializer(posts, many=True,  context={'request': request}) 
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_posts_view(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user 
        post.save()
        image_url , video_url= None, None
        if post and post.image:
            image_url = request.build_absolute_uri(post.image.url)

        if post and post.video:
            video_url = request.build_absolute_uri(post.video.url)

        return JsonResponse({
            "status": status.HTTP_201_CREATED,
            "id": post.id,
            "user": post.user.id,
            "title": post.title,
            "content": post.content,
            "image": image_url,
            "video": video_url,
            "date": post.date,
            "message": "Create is success"
        })
    else:
        errors = {field: " ".join([str(e) for e in errs]) for field, errs in form.errors.items()}
        return JsonResponse({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": errors
        })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_posts_view(request, pk):
    post = Post.objects.filter(pk=pk, user=request.user).first()

    if not post:
        return JsonResponse({
            "status": status.HTTP_404_NOT_FOUND,
            "message": "ID is not found or not owner"
        }, status=status.HTTP_404_NOT_FOUND)

    # Django forms do NOT support PUT directly, so convert PUT to POST
    data = request.data.copy()

    form = PostForm(data, request.FILES, instance=post)

    if form.is_valid():
        updated_post = form.save()

        image_url = request.build_absolute_uri(updated_post.image.url) if updated_post.image else None
        video_url = request.build_absolute_uri(updated_post.video.url) if updated_post.video else None

        return JsonResponse({
            "status": status.HTTP_200_OK,
            "id": updated_post.id,
            "user": updated_post.user.id,
            "title": updated_post.title,
            "content": updated_post.content,
            "image": image_url,
            "video": video_url,
            "date": updated_post.date,
            "message": "Update success"
        }, status=status.HTTP_200_OK)

    errors = {field: " ".join([str(e) for e in errs]) for field, errs in form.errors.items()}
    return JsonResponse({
        "status": status.HTTP_400_BAD_REQUEST,
        "errors": errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_posts_view(request, pk):
    import os
    post = Post.objects.filter(pk=pk, user=request.user).first()
    if post:
        if post.image and os.path.isfile(post.image.path):
            os.remove(post.image.path)
        
        if post.video and os.path.isfile(post.video.path):
            os.remove(post.video.path)
        post.delete()
        return JsonResponse({"status": status.HTTP_200_OK, "message": "Delete is sucess"})
    else:
        return JsonResponse({"status": status.HTTP_404_NOT_FOUND, "message": "ID is not found or not owner"})



@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def like_api(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post:
        like = Like.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
            return JsonResponse({"status": status.HTTP_200_OK, "message": "Unliked"})
        else:
            Like.objects.create(post=post, user=request.user)
            return JsonResponse({"status": status.HTTP_200_OK, "message": "Liked"})
    else:
        return JsonResponse({"status": status.HTTP_404_NOT_FOUND, "message": "ID is not found."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_api(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse(
            {"status": status.HTTP_404_NOT_FOUND, "message": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    comment_text = request.data.get('comment')
    if not comment_text:
        return JsonResponse(
            {"status": status.HTTP_400_BAD_REQUEST, "message": "Comment cannot be empty"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if len(comment_text) > 500:
        return JsonResponse(
            {"status": status.HTTP_400_BAD_REQUEST, "message": "Cannot input more than 500 charactors"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        comment = Comment.objects.create(user=request.user, post=post, content=comment_text)
        return JsonResponse(
            {"status": status.HTTP_201_CREATED, "message": "Comment added successfully", "id": comment.id},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        print(e)
        return JsonResponse(
            {"status": status.HTTP_400_BAD_REQUEST, "message": "Something went wrong"},
            status=status.HTTP_400_BAD_REQUEST
        )
