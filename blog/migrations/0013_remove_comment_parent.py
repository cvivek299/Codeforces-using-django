# Generated by Django 2.1 on 2019-01-19 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]
