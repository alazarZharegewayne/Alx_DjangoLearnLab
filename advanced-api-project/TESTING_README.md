# API Testing Documentation

## Overview
This document describes the comprehensive test suite for the Django REST Framework API, covering all endpoints, functionality, and edge cases.

## Test Structure

### Test Classes
- **BaseTestCase**: Base class with common setup and test data
- **BookListViewTests**: Tests for book listing, filtering, searching, ordering
- **BookDetailViewTests**: Tests for single book retrieval
- **BookCreateViewTests**: Tests for book creation with validation
- **BookUpdateViewTests**: Tests for book updates
- **BookDeleteViewTests**: Tests for book deletion
- **AuthorViewTests**: Tests for author endpoints with nested books
- **PermissionTests**: Tests for authentication and permission enforcement

## Test Coverage

### Book Endpoints
✅ List all books (with filtering, searching, ordering)  
✅ Retrieve single book  
✅ Create new book (authenticated only)  
✅ Update existing book (authenticated only)  
✅ Delete book (authenticated only)  

### Author Endpoints
✅ List all authors with nested books  
✅ Retrieve single author with nested books  

### Features Tested
✅ CRUD operations  
✅ Filtering by title, author, publication year  
✅ Searching across title and author fields  
✅ Ordering by various fields  
✅ Authentication and permissions  
✅ Data validation (publication year)  
✅ Error handling (404, 403, 400)  

## Running Tests

### Basic Test Execution
```bash
# Run all tests
python manage.py test api

# Run with verbose output
python manage.py test api --verbosity=2

# Run specific test class
python manage.py test api.tests.BookListViewTests

# Run specific test method
python manage.py test api.tests.BookListViewTests.test_filter_books_by_author_name
