# Generated by Django 2.1.4 on 2019-01-04 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='updated',
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(null=True),
        ),
    ]