# Generated by Django 3.1.7 on 2021-05-29 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210513_1002'),
        ('warehouse', '0013_auto_20210308_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouses', to='store.store'),
        ),
    ]
