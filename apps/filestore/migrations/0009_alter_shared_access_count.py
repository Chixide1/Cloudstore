# Generated by Django 5.0.7 on 2024-07-21 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filestore', '0008_remove_shared_url_shared_access_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shared',
            name='access_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
