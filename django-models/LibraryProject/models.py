from django.db import models
from django.contrib.auth.models import User

# Your existing UserProfile model
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Add the missing models if needed
class Author(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Add other fields as needed

class Library(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    # Add other fields as needed

# Signals for UserProfile (keep these)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
