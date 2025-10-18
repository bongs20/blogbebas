from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_category_created_at_category_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
