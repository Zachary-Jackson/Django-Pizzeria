# Generated by Django 2.1.2 on 2018-10-30 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0002_auto_20181030_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='crust',
            field=models.ForeignKey(on_delete='cascade', to='workshop.Crust'),
        ),
    ]