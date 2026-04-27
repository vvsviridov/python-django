from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.last()
        group, created = Group.objects.get_or_create(name='profile_manager')
        permission_profile, created = Permission.objects.get_or_create(
            codename='view_profile'
        )
        permission_logentry, created = Permission.objects.get_or_create(
            codename='view_logentry'
        )
        group.permissions.add(permission_profile)
        user.groups.add(group)
        user.user_permissions.add(permission_logentry)
        group.save()
        user.save()
