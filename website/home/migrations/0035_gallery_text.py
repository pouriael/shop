# Generated by Django 4.0.4 on 2022-07-23 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='text',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]