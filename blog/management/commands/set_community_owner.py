from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from blog.models import Category


class Command(BaseCommand):
    help = "Set a user as owner/creator for communities (Komunitas). Adds as moderator as well."

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Username to set as owner')
        parser.add_argument('--all', action='store_true', help='Apply to all communities')
        parser.add_argument('--slugs', help='Comma-separated list of community slugs to update')

    def handle(self, *args, **options):
        username = options['username']
        apply_all = options['all']
        slugs = options.get('slugs')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User {username!r} not found')

        qs = Category.objects.all()
        if slugs:
            slug_list = [s.strip() for s in slugs.split(',') if s.strip()]
            qs = qs.filter(slug__in=slug_list)
        elif not apply_all:
            # default: only those without owner
            qs = qs.filter(created_by__isnull=True)

        updated = 0
        for c in qs:
            c.created_by = user
            c.save(update_fields=['created_by'])
            c.moderators.add(user)
            updated += 1
        self.stdout.write(self.style.SUCCESS(f'Updated owner for {updated} communities to {username}'))
