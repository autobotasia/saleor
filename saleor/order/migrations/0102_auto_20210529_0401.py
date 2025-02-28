# Generated by Django 3.1.7 on 2021-05-29 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210513_1002'),
        ('order', '0101_auto_20210308_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulfillment',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fulfillments', to='store.store'),
        ),
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='store.store'),
        ),
    ]
