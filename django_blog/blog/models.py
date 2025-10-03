from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    """
    Post model representing a blog post.
    Each post has a title, content, publication date, and author.
    The author is linked to Django's built-in User model.
    """
    title = models.CharField(max_length=200, help_text="Title of the blog post")
    content = models.TextField(help_text="Main content of the blog post")
    published_date = models.DateTimeField(auto_now_add=True, help_text="Date when the post was published")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts',
        help_text="Author who wrote this post"
    )

    def __str__(self):
        """String representation of the Post model"""
        return f"{self.title} by {self.author.username}"

    def get_absolute_url(self):
        """Returns the URL to access a particular post instance"""
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        """Metadata for the Post model"""
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_date']  # Newest posts first
