# Generated by Django 3.0.6 on 2020-06-09 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPCD', '0006_auto_20200609_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='Rank',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='ScholarshipValue',
            field=models.FloatField(default=None),
        ),
    ]
