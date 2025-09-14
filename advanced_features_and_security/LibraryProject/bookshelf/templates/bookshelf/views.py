from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from .models import Book
from .forms import BookForm

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
    return render(request, 'bookshelf:delete_book.html', {'book': book})

# Secure file upload view example
@login_required
def secure_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Validate file type and size
        if uploaded_file.content_type not in ['image/jpeg', 'image/png']:
            return HttpResponseBadRequest("Invalid file type")
        
        if uploaded_file.size > 5 * 1024 * 1024:  # 5MB limit
            return HttpResponseBadRequest("File too large")
        
        # Process the secure file
        return redirect('bookshelf:book_list')
    
    return render(request, 'bookshelf/upload.html')
