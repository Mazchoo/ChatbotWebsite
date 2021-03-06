# Generated by Django 3.1.4 on 2020-12-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20201221_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='stories',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='vocabs',
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
