# Generated by Django 2.2.4 on 2020-05-19 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPCD', '0002_auto_20200517_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='Class',
            field=models.CharField(default=None, max_length=3),
            preserve_default=False,
        ),
    ]
