# Generated by Django 3.1.2 on 2020-10-03 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_blogcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timeStamps',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 3, 17, 34, 1, 832566)),
        ),
    ]
