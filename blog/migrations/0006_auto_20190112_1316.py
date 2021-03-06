# Generated by Django 2.1 on 2019-01-12 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190110_1334'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blogcomment',
            unique_together={('blog', 'comment')},
        ),
        migrations.AlterUniqueTogether(
            name='userblog',
            unique_together={('user', 'blog')},
        ),
        migrations.AlterUniqueTogether(
            name='usercomment',
            unique_together={('user', 'comment')},
        ),
    ]
