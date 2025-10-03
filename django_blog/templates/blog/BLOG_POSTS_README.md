# Blog Post Management Features

## Overview
Complete CRUD (Create, Read, Update, Delete) operations for blog posts with proper authentication and authorization.

## Features

### 1. Read Operations
- **List View**: Display all blog posts with pagination
- **Detail View**: Show individual post with author information
- **Public Access**: Anyone can read posts without authentication

### 2. Create Operations
- **Create View**: Authenticated users can create new posts
- **Auto Author Assignment**: Posts automatically assigned to logged-in user
- **Form Validation**: Title and content validation

### 3. Update Operations
- **Update View**: Post authors can edit their own posts
- **Permission Check**: Only post author can edit
- **Success Messages**: User feedback after updates

### 4. Delete Operations
- **Delete View**: Post authors can delete their own posts
- **Confirmation**: Double confirmation before deletion
- **Security**: Prevents unauthorized deletion

## URL Patterns

- `/posts/` - List all posts (PostListView)
- `/posts/<int:pk>/` - View single post (PostDetailView)
- `/posts/new/` - Create new post (PostCreateView) - Login required
- `/posts/<int:pk>/update/` - Edit post (PostUpdateView) - Author required
- `/posts/<int:pk>/delete/` - Delete post (PostDeleteView) - Author required

## Permissions

- **Public**: List and detail views accessible to all
- **Authenticated Users**: Can create posts
- **Post Authors**: Can update and delete their own posts
- **Security**: Uses Django's LoginRequiredMixin and UserPassesTestMixin

## Testing

1. **Create Post**: Login → Click "Write New Post" → Fill form → Submit
2. **Read Posts**: Visit `/posts/` to see all posts
3. **Update Post**: As author → Click "Edit" on your post → Modify → Save
4. **Delete Post**: As author → Click "Delete" → Confirm deletion

## Templates

- `post_list.html` - Paginated list of all posts
- `post_detail.html` - Individual post with author info
- `post_form.html` - Create/Edit post form
