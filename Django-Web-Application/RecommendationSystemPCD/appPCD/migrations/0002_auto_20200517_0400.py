# Generated by Django 2.2.4 on 2020-05-17 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPCD', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
