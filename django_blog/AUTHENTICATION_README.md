# Django Blog Authentication System Documentation

## Overview
The Django Blog authentication system provides comprehensive user management including registration, login, logout, and profile management. The system uses Django's built-in authentication framework with custom extensions.

## Features

### 1. User Registration
- **URL**: `/register/`
- **Features**:
  - Custom registration form extending `UserCreationForm`
  - Additional fields: email, first name, last name
  - Automatic login after successful registration
  - Email uniqueness validation
  - Password strength validation

### 2. User Login
- **URL**: `/login/`
- **Features**:
  - Uses Django's `AuthenticationForm`
  - Redirects to intended page after login
  - Error messages for invalid credentials
  - CSRF protection

### 3. User Logout
- **URL**: `/logout/`
- **Features**:
  - Secure session termination
  - Success message feedback
  - Redirect to home page

### 4. Profile Management
- **URL**: `/profile/`
- **Features**:
  - View and update user information
  - Email uniqueness validation
  - Display user's blog posts
  - Quick access to post management

### 5. Post Management
- **Create Post**: `/posts/new/` (Authenticated users only)
- **Update Post**: `/posts/<id>/edit/` (Post authors only)
- **Delete Post**: `/posts/<id>/delete/` (Post authors only)

## Security Features

### CSRF Protection
All forms include CSRF tokens to prevent Cross-Site Request Forgery attacks.

```html
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
