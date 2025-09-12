from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import CustomUser

class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(CustomUser)
        
        viewers, created = Group.objects.get_or_create(name='Viewers')
        editors, created = Group.objects.get_or_create(name='Editors')
        admins, created = Group.objects.get_or_create(name='Admins')
        
        viewers.permissions.set([
            Permission.objects.get(codename='can_view_dashboard'),
        ])
        
        editors.permissions.set([
            Permission.objects.get(codename='can_view_dashboard'),
            Permission.objects.get(codename='can_create_content'),
            Permission.objects.get(codename='can_edit_content'),
        ])
        
        admins.permissions.set([
            Permission.objects.get(codename='can_view_dashboard'),
            Permission.objects.get(codename='can_create_content'),
            Permission.objects.get(codename='can_edit_content'),
            Permission.objects.get(codename='can_delete_content'),
        ])
        
        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions'))
