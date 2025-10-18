from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Category, Post, Comment, Vote
from random import choice, randint


class Command(BaseCommand):
    help = 'Seed demo users, categories, posts, comments, and votes'

    def handle(self, *args, **options):
        # Users
        admin, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
        if not admin.password:
            admin.set_password('admin123')
            admin.save()

        users = []
        for uname in ['alice', 'bob', 'charlie', 'diana', 'eric']:
            u, _ = User.objects.get_or_create(username=uname)
            if not u.password:
                u.set_password('password')
                u.save()
            users.append(u)

        # Categories
        names = ['General', 'News', 'Technology', 'Programming', 'Gaming', 'Science', 'Music', 'Movies', 'Sports', 'Art']
        cats = []
        for n in names:
            c, _ = Category.objects.get_or_create(slug=slugify(n), defaults={'name': n, 'is_verified': True})
            cats.append(c)

        # Posts
        sample_posts = [
            'Check this out', 'Hello World', 'My first post', 'Django tips', 'Ask anything', 'Weekly thread', 'Interesting article',
        ]
        for _ in range(20):
            author = choice(users)
            cat = choice(cats)
            title = choice(sample_posts)
            content = 'This is a demo content for %s in r/%s' % (author.username, cat.slug)
            post = Post.objects.create(author=author, category=cat, title=title, content=content)
            # Comments
            for _ in range(randint(0, 3)):
                Comment.objects.create(post=post, author=choice(users), content='Nice post!')
            # Votes
            for u in users:
                if randint(0, 1):
                    Vote.objects.get_or_create(post=post, user=u, defaults={'value': choice([1, -1])})

        self.stdout.write(self.style.SUCCESS('Demo data seeded.'))
