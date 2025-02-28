# Generated by Django 3.1.7 on 2021-05-10 07:38

import django.contrib.postgres.indexes
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import saleor.core.db.fields
import saleor.core.utils.editorjs
import saleor.core.utils.json_serializer
import saleor.store.models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_metadata', models.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=70, null=True, validators=[django.core.validators.MaxLengthValidator(70)])),
                ('seo_description', models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('name', models.CharField(max_length=250)),
                ('description', saleor.core.db.fields.SanitizedJSONField(blank=True, null=True, sanitizer=saleor.core.utils.editorjs.clean_editor_js)),
                ('phone', saleor.store.models.PossiblePhoneNumberField(blank=True, default='', max_length=128, region=None)),
                ('acreage', models.FloatField(blank=True, max_length=250, null=True)),
                ('latlong', models.CharField(blank=True, max_length=250, null=True)),
                ('background_image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='store-backgrounds')),
                ('background_image_alt', models.CharField(blank=True, max_length=128, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'ordering': ('name', 'pk'),
                'permissions': (('manage_stores', 'Manage store.'),),
            },
        ),
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_metadata', models.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=70, null=True, validators=[django.core.validators.MaxLengthValidator(70)])),
                ('seo_description', models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('name', models.CharField(max_length=250)),
                ('description', saleor.core.db.fields.SanitizedJSONField(blank=True, null=True, sanitizer=saleor.core.utils.editorjs.clean_editor_js)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.storetype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_title', models.CharField(blank=True, max_length=70, null=True, validators=[django.core.validators.MaxLengthValidator(70)])),
                ('seo_description', models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('language_code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=128)),
                ('description', saleor.core.db.fields.SanitizedJSONField(blank=True, null=True, sanitizer=saleor.core.utils.editorjs.clean_editor_js)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='store.store')),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='store_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='store.storetype'),
        ),
        migrations.CreateModel(
            name='StoreTypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_title', models.CharField(blank=True, max_length=70, null=True, validators=[django.core.validators.MaxLengthValidator(70)])),
                ('seo_description', models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('language_code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=128)),
                ('description', saleor.core.db.fields.SanitizedJSONField(blank=True, null=True, sanitizer=saleor.core.utils.editorjs.clean_editor_js)),
                ('store_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='store.storetype')),
            ],
            options={
                'unique_together': {('language_code', 'store_type')},
            },
        ),
        migrations.AddIndex(
            model_name='storetype',
            index=django.contrib.postgres.indexes.GinIndex(fields=['private_metadata'], name='storetype_p_meta_idx'),
        ),
        migrations.AddIndex(
            model_name='storetype',
            index=django.contrib.postgres.indexes.GinIndex(fields=['metadata'], name='storetype_meta_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='storetranslation',
            unique_together={('language_code', 'store')},
        ),
    ]
