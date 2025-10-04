from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the blog post")
    content = models.TextField(help_text="Main content of the blog post")
    published_date = models.DateTimeField(auto_now_add=True, help_text="Date when the post was published")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts',
        help_text="Author who wrote this post"
    )
    # Add tagging functionality
    tags = TaggableManager(blank=True, help_text="Tags for categorizing the post")

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_date']


class Comment(models.Model):
    """
    Comment model representing user comments on blog posts.
    Each comment is linked to a specific post and user (author).
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Post that this comment belongs to"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_comments',
        help_text="User who wrote this comment"
    )
    content = models.TextField(
        max_length=1000,
        help_text="Content of the comment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the comment was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the comment was last updated"
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at']
