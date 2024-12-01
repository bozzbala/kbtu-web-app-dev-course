from django.shortcuts import render, get_object_or_404
from .models import Post

def posts(request):
    posts = Post.published.all()
    return render(request, 'blog/templates/posts.html', {'posts': posts})

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/templates/post.html', {'post': post})
