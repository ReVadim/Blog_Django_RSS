from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


class PostListView(ListView):
    """ Class-based view to list posts
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3


def post_detail(request, year, month, day, post):
    """ Detail information about post
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }

    return render(request, 'blog/post/detail.html', context=context)


def post_share(request, post_id):
    """ Published post by id
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{data['name']}\'s comments: {data['comments']}"
            send_mail(subject, message, 'revani.web@gmail.com', [data['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


# for POST method only
@require_POST
def post_comment(request, post_id):
    """ add comment to post and render than
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create comment object without saving it in the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save to the database
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }

    return render(request, 'blog/post/comment.html', context=context)
