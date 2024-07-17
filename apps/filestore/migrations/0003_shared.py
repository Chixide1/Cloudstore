# Generated by Django 5.0.7 on 2024-07-17 21:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filestore', '0002_alter_file_file_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shared',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(null=True)),
                ('access_count', models.IntegerField(default=0)),
                ('file', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='filestore.file')),
            ],
        ),
    ]
