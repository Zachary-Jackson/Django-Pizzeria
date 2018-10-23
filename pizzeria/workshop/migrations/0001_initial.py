# Generated by Django 2.1.2 on 2018-10-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('likes', models.IntegerField()),
                ('dislikes', models.IntegerField()),
                ('crust', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=40)),
                ('summary', models.CharField(max_length=200)),
                ('time_created', models.DateTimeField(auto_now=True)),
                ('ingredients', models.ManyToManyField(to='workshop.Ingredient')),
            ],
        ),
    ]
