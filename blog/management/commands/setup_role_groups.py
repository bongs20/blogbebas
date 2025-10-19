from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from blog.utils import GROUP_WEBSITE_ADMINS, GROUP_ACTIVE, GROUP_COMMUNITY_MODS


class Command(BaseCommand):
    help = 'Create default role groups and optionally assign users to them.'

    def add_arguments(self, parser):
        parser.add_argument('--website-admins', help='Comma-separated usernames to add to Website Admins')
        parser.add_argument('--active', help='Comma-separated usernames to add to Active')
        parser.add_argument('--community-mods', help='Comma-separated usernames to add to Community Moderators')

    def handle(self, *args, **options):
        g_admins, _ = Group.objects.get_or_create(name=GROUP_WEBSITE_ADMINS)
        g_active, _ = Group.objects.get_or_create(name=GROUP_ACTIVE)
        g_mods, _ = Group.objects.get_or_create(name=GROUP_COMMUNITY_MODS)
        self.stdout.write(self.style.SUCCESS('Ensured role groups exist.'))

        def assign(group, users_str):
            if not users_str:
                return
            for uname in [s.strip() for s in users_str.split(',') if s.strip()]:
                try:
                    u = User.objects.get(username=uname)
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'User {uname!r} not found'))
                    continue
                u.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Added {uname} to {group.name}'))

        assign(g_admins, options.get('website_admins'))
        assign(g_active, options.get('active'))
        assign(g_mods, options.get('community_mods'))
