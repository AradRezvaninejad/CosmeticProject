from django.shortcuts import render
from .models import Post
from django.shortcuts import render, get_object_or_404

def index(request):
    posts = Post.objects.all().order_by('-created_at')  
    return render(request, "Blog/Blog.html", {'posts': posts})  

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'Blog/post.html', {'post': post})