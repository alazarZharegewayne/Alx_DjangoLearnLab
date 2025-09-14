from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Book, Author
from .forms import BookForm, ExampleForm, SearchForm  # ADD ExampleForm HERE

@login_required
def book_list(request):
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
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
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# Example form view
@login_required
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            return render(request, 'bookshelf/form_success.html', {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email']
            })
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

# Secure search
@login_required
def secure_search_api(request):
    if request.method == 'GET':
        search_term = request.GET.get('q', '').strip()
        
        if not search_term or len(search_term) > 100:
            return JsonResponse({'error': 'Invalid search term'}, status=400)
        
        books = Book.objects.filter(
            Q(title__icontains=search_term) | 
            Q(author__name__icontains=search_term)
        )[:10]
        
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

def form_success(request):
    return render(request, 'bookshelf/form_success.html')

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z',
        'version': '1.0.0'
    })
