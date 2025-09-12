# Permissions and Groups Setup

## Groups:
- **Viewers**: can_view_dashboard
- **Editors**: can_view_dashboard, can_create_content, can_edit_content  
- **Admins**: All permissions

## Setup:
1. Run: `python manage.py setup_groups`
2. Assign users to groups in Django Admin

## Usage in Views:
```python
@permission_required('bookshelf.can_create_content')
def create_view(request):
    # view code
