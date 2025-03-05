# Generated by Django 5.1.5 on 2025-03-05 07:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0009_alter_comments_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replies',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('comment_id', models.CharField(max_length=100)),
                ('reply', models.CharField(max_length=100)),
            ],
        ),
    ]
