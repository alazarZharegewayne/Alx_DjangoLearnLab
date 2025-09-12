from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from bookshelf.models import CustomUser

class PermissionTests(TestCase):
    def setUp(self):
        self.viewer = CustomUser.objects.create_user(email='viewer@test.com', password='testpass')
        self.editor = CustomUser.objects.create_user(email='editor@test.com', password='testpass')
        self.admin = CustomUser.objects.create_user(email='admin@test.com', password='testpass')
        
        viewer_group = Group.objects.get(name='Viewers')
        editor_group = Group.objects.get(name='Editors')
        admin_group = Group.objects.get(name='Admins')
        
        self.viewer.groups.add(viewer_group)
        self.editor.groups.add(editor_group)
        self.admin.groups.add(admin_group)
    
    def test_viewer_permissions(self):
        self.assertTrue(self.viewer.has_perm('bookshelf.can_view_dashboard'))
        self.assertFalse(self.viewer.has_perm('bookshelf.can_create_content'))
    
    def test_editor_permissions(self):
        self.assertTrue(self.editor.has_perm('bookshelf.can_view_dashboard'))
        self.assertTrue(self.editor.has_perm('bookshelf.can_create_content'))
        self.assertFalse(self.editor.has_perm('bookshelf.can_delete_content'))
    
    def test_admin_permissions(self):
        self.assertTrue(self.admin.has_perm('bookshelf.can_view_dashboard'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_create_content'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_delete_content'))
