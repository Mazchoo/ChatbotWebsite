# Generated by Django 3.1.4 on 2021-07-10 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210508_1621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vocabalteration',
            old_name='bot_name',
            new_name='bot',
        ),
    ]