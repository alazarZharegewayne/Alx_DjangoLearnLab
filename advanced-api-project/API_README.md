# Django REST Framework API Documentation

## Overview
This API provides CRUD operations for Books and Authors with proper authentication and permissions.

## API Endpoints

### Books
- `GET /api/books/` - List all books (Public)
- `GET /api/books/<id>/` - Get book details (Public)
- `POST /api/books/create/` - Create new book (Authenticated only)
- `PUT /api/books/<id>/update/` - Update book (Authenticated only)
- `DELETE /api/books/<id>/delete/` - Delete book (Authenticated only)

### Authors
- `GET /api/authors/` - List all authors (Public)
- `GET /api/authors/<id>/` - Get author details with nested books (Public)

## Authentication & Permissions
- **Public Access**: List and retrieve operations don't require authentication
- **Authenticated Access**: Create, update, and delete operations require user authentication
- **Permissions**: Implemented using DRF's permission classes

## View Configuration
- **Generic Views**: Used ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
- **Custom Validation**: Publication year validation in BookSerializer
- **Nested Serialization**: Authors include their books in responses
- **Pagination**: Results are paginated with 10 items per page

## Testing
Use the provided test script or tools like curl/Postman to test all endpoints.
