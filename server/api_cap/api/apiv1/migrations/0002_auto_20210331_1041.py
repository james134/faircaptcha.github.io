# Generated by Django 3.1.7 on 2021-03-31 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiv1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='client',
        ),
        migrations.AddField(
            model_name='client',
            name='signals',
            field=models.ManyToManyField(to='apiv1.Signal'),
        ),
    ]
