# Generated by Django 5.1.5 on 2025-03-03 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0007_followers_delete_follow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=100)),
                ('post_id', models.CharField(max_length=500)),
                ('user', models.CharField(max_length=20)),
            ],
        ),
    ]
