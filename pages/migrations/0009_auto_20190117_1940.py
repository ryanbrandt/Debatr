# Generated by Django 2.1.4 on 2019-01-18 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_post_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
    ]
