# Generated by Django 3.1.7 on 2021-05-05 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0023_page_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagemedia',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
