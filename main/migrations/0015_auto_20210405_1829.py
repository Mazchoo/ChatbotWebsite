# Generated by Django 3.1.4 on 2021-04-05 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210405_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatlog',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
