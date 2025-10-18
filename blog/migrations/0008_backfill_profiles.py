from django.db import migrations


def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('blog', 'UserProfile')
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_userprofile'),
    ]

    operations = [
        migrations.RunPython(create_profiles, reverse_code=migrations.RunPython.noop),
    ]
