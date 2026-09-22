from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, PostForm, CommentForm, ProfileEditForm
from .models import User, Post, Follow


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to the community, {user.username}!")
            return redirect('feed')
    else:
        form = RegisterForm()

    return render(request, 'social/register.html', {'form': form})


@login_required
def feed(request):
    """Shows posts from people the current user follows, plus their own posts."""
    following_ids = request.user.following.values_list('following_id', flat=True)
    posts = Post.objects.filter(
        Q(author_id__in=following_ids) | Q(author=request.user)
    ).select_related('author')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post published!")
            return redirect('feed')
    else:
        form = PostForm()

    suggested_users = User.objects.exclude(
        id__in=list(following_ids) + [request.user.id]
    )[:5]

    return render(request, 'social/feed.html', {
        'posts': posts,
        'form': form,
        'suggested_users': suggested_users,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post published!")
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social/create_post.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
    comments = post.comments.select_related('author')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'social/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def toggle_like(request, pk):
    """AJAX endpoint: like/unlike a post. Returns JSON so the page doesn't reload."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    post = get_object_or_404(Post, pk=pk)
    like_qs = post.likes.filter(user=request.user)

    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        post.likes.create(user=request.user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_count()})


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()
    is_following = request.user.is_following(profile_user) if request.user != profile_user else None

    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    })


@login_required
def toggle_follow(request, username):
    """AJAX endpoint: follow/unfollow a user."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    target = get_object_or_404(User, username=username)

    if target == request.user:
        return JsonResponse({'error': "You can't follow yourself."}, status=400)

    follow_qs = Follow.objects.filter(follower=request.user, following=target)

    if follow_qs.exists():
        follow_qs.delete()
        following = False
    else:
        Follow.objects.create(follower=request.user, following=target)
        following = True

    return JsonResponse({
        'following': following,
        'follower_count': target.follower_count(),
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'social/edit_profile.html', {'form': form})


@login_required
def explore(request):
    """A simple directory of all users, so people have someone to follow."""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'social/explore.html', {'users': users})
