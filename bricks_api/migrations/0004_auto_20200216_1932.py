# Generated by Django 2.2.3 on 2020-02-16 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bricks_api', '0003_auto_20200216_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='date_start',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
    ]
