from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


def post_list(request):
    """ display all posts
    """
    posts = Post.published.all()

    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, post_id):
    """ Detail information about post
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post/detail.html', {'post': post})
