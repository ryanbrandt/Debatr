# Generated by Django 2.1.4 on 2019-01-16 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_profile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('LFD', 'Looking for a debate'), ('FYC', 'For your consideration'), ('SI', 'Seeking information')], default=None, max_length=1),
            preserve_default=False,
        ),
    ]
