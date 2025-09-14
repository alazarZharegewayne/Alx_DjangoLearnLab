from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Book, Author
from .forms import BookForm, ExampleForm, SearchForm

@login_required
def book_list(request):
    # Secure search functionality - prevents SQL injection
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        # Use Django ORM to safely filter (parameterized queries)
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__name__icontains=search_query)
        )
    else:
        books = Book.objects.all()
    
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, book_id):
    # Safe object retrieval with get_object_or_404
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    # Safe object retrieval
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# Example form view for security demonstration
@login_required
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process validated data safely
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # Secure processing - no direct template rendering of user input
            return render(request, 'bookshelf/form_success.html', {
                'name': name,
                'email': email  # This is safe because it's validated
            })
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

# Secure search API endpoint
@login_required
def secure_search_api(request):
    if request.method == 'GET':
        search_term = request.GET.get('q', '').strip()
        
        # Input validation and sanitization
        if not search_term or len(search_term) > 100:
            return JsonResponse({'error': 'Invalid search term'}, status=400)
        
        # Safe ORM query - prevents SQL injection
        books = Book.objects.filter(
            Q(title__icontains=search_term) | 
            Q(author__name__icontains=search_term)
        )[:10]  # Limit results for security
        
        results = [
            {
                'title': book.title,
                'author': book.author.name,
                'id': book.id
            }
            for book in books
        ]
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Secure file upload example
@login_required
def secure_file_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Validate file type and size
        allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
        if uploaded_file.content_type not in allowed_types:
            return HttpResponseBadRequest("Invalid file type. Allowed: JPEG, PNG, PDF")
        
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB limit
            return HttpResponseBadRequest("File size exceeds 10MB limit")
        
        # Validate filename security
        import re
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', uploaded_file.name):
            return HttpResponseBadRequest("Invalid filename")
        
        # Process the secure file (would save to secure location in real implementation)
        return JsonResponse({
            'status': 'success',
            'filename': uploaded_file.name,
            'size': uploaded_file.size,
            'type': uploaded_file.content_type
        })
    
    return render(request, 'bookshelf/upload.html')

# Health check endpoint (safe from injections)
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z',  # Hardcoded safe value
        'version': '1.0.0'
    })
