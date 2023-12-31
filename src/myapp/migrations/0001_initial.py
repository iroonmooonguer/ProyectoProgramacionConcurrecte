# Generated by Django 4.1.13 on 2023-11-29 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('organizer', models.CharField(max_length=255)),
                ('time', models.TimeField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagen', models.TextField(blank=True)),
            ],
        ),
    ]
