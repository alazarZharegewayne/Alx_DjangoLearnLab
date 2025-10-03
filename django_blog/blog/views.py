from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post

def home(request):
    """
    Home page view showing latest posts and blog statistics
    """
    latest_posts = Post.objects.all().order_by('-published_date')[:5]
    total_posts = Post.objects.count()
    total_authors = User.objects.count()
    
    context = {
        'posts': latest_posts,
        'total_posts': total_posts,
        'total_authors': total_authors,
    }
    
    return render(request, 'blog/home.html', context)

def post_list(request):
    """
    View to display all blog posts
    """
    posts = Post.objects.all().order_by('-published_date')
    
    context = {
        'posts': posts,
    }
    
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    """
    View to display a single blog post
    """
    post = get_object_or_404(Post, pk=pk)
    
    context = {
        'post': post,
    }
    
    return render(request, 'blog/post_detail.html', context)
