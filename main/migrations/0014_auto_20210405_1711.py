# Generated by Django 3.1.4 on 2021-04-05 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_chatlog_text_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatlog',
            name='icon_name',
        ),
        migrations.AddField(
            model_name='chatlog',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]