from django.db import migrations, models


def migrate_approval_to_verified(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    if not hasattr(Category, 'is_verified'):
        return
    for cat in Category.objects.all():
        if hasattr(cat, 'is_approved'):
            cat.is_verified = bool(getattr(cat, 'is_approved'))
            cat.save(update_fields=['is_verified'])


def seed_default_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    defaults = [
        ('general', 'General'),
        ('news', 'News'),
        ('technology', 'Technology'),
        ('programming', 'Programming'),
        ('gaming', 'Gaming'),
        ('science', 'Science'),
        ('music', 'Music'),
        ('movies', 'Movies'),
        ('sports', 'Sports'),
        ('art', 'Art'),
    ]
    for slug, name in defaults:
        Category.objects.get_or_create(slug=slug, defaults={'name': name, 'is_verified': True})


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_category_is_verified_seed_defaults'),
    ]

    operations = [
        migrations.RunPython(migrate_approval_to_verified, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(seed_default_categories, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='category',
            name='is_approved',
        ),
    ]
