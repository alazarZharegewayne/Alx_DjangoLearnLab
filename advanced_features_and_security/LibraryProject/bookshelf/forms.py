from django import forms
from django.core.exceptions import ValidationError
from .models import Book, CustomUser
import re

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 2:
            raise ValidationError("Title must be at least 2 characters long.")
        return title

class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        }),
        error_messages={'required': 'Please enter your name'}
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        }),
        required=False
    )

    age = forms.IntegerField(
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )

    agree_to_terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the terms'}
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and not re.match(r'^[a-zA-Z\s]+$', name):
            raise ValidationError("Name can only contain letters and spaces.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith(('.com', '.org', '.net')):
            raise ValidationError("Please enter a valid email address.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob.year < 1900:
            raise ValidationError("Please enter a valid date of birth.")
        return dob

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...'
        })
    )
    
    search_by = forms.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('author', 'Author'),
            ('both', 'Both')
        ],
        initial='both',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
