from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Post
from .forms import UserRegisterForm, UserUpdateForm, PostForm

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

def register(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Auto-login after registration
            login(request, user)
            
            messages.success(request, f'Account created successfully! Welcome, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    
    # Use dedicated register template
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    """
    User login view
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next page if provided, otherwise home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    # Add Bootstrap classes to login form
    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})
    
    # Use dedicated login template
    return render(request, 'blog/login.html', {'form': form})

@login_required
def user_logout(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def profile(request):
    """
    User profile view - allows users to view and update their profile
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Get user's posts for display
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'form': form,
        'user_posts': user_posts,
        'title': 'My Profile'
    }
    
    return render(request, 'blog/profile.html', context)

@login_required
def post_create(request):
    """
    View for creating new blog posts
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post-detail', pk=post.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Create New Post'
    }
    
    return render(request, 'blog/post_form.html', context)

@login_required
def post_update(request, pk):
    """
    View for updating existing blog posts
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the current user is the author of the post
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post-detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('post-detail', pk=post.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'title': 'Edit Post',
        'post': post
    }
    
    return render(request, 'blog/post_form.html', context)

@login_required
def post_delete(request, pk):
    """
    View for deleting blog posts
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the current user is the author of the post
    if post.author != request.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post-detail', pk=post.pk)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" has been deleted successfully!')
        return redirect('home')
    
    context = {
        'post': post,
        'title': 'Delete Post'
    }
    
    return render(request, 'blog/post_confirm_delete.html', context)

def test_static_files(request):
    """
    Test view to verify static files are loading correctly
    """
    return render(request, 'blog/test_static.html')
