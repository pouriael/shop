# Generated by Django 4.0.4 on 2022-07-07 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='emial',
            new_name='email',
        ),
    ]