# Generated by Django 2.1.4 on 2019-01-16 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20190115_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('', '--'), ('LFD', 'Looking for a debate'), ('FYC', 'For your consideration'), ('SI', 'Seeking information')], max_length=1),
        ),
    ]
