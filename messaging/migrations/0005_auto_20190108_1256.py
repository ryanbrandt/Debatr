# Generated by Django 2.1.4 on 2019-01-08 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_auto_20190108_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
