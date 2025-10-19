from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from blog.utils import GROUP_WEBSITE_ADMINS


class Command(BaseCommand):
    help = 'Promote a user to Website Admin (is_staff, optional superuser) and add to Website Admins group.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--password', help='Set/reset password (optional)')
        parser.add_argument('--superuser', action='store_true', help='Also grant superuser')

    def handle(self, *args, **options):
        username = options['username']
        password = options.get('password')
        make_super = options.get('superuser', False)

        user, created = User.objects.get_or_create(username=username)
        if created:
            self.stdout.write(self.style.WARNING(f'User {username!r} did not exist. Created a new user.'))
        if password:
            user.set_password(password)
        user.is_staff = True
        if make_super:
            user.is_superuser = True
        user.save()

        group, _ = Group.objects.get_or_create(name=GROUP_WEBSITE_ADMINS)
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            f"Promoted {username} to Website Admin (staff={'yes'}, superuser={'yes' if make_super else 'no'})"
        ))
