# Generated by Django 5.2 on 2025-05-11 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapapp', '0009_alter_mappin_category_alter_mappin_is_accessible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappin',
            name='is_accessible',
            field=models.BooleanField(default=True),
        ),
    ]
