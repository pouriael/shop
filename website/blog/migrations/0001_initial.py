# Generated by Django 4.0.4 on 2022-08-10 16:09

import ckeditor_uploader.fields
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='اسم')),
                ('create', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('update', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='blog')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
        ),
    ]
