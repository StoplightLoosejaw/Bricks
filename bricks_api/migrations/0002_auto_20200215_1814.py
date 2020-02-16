# Generated by Django 2.2.3 on 2020-02-15 15:14

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bricks_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='date_updated',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brick_task',
            name='bricks',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='house',
            name='date_last_load',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='total_bricks_required',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]