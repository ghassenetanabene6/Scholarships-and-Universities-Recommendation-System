# Generated by Django 2.2.4 on 2020-05-22 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPCD', '0003_scholarship_class'),
    ]

    operations = [
        migrations.CreateModel(
            name='historique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('classe', models.CharField(max_length=3)),
            ],
        ),
    ]
