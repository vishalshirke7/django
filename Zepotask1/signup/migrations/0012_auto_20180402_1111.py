# Generated by Django 2.0.3 on 2018-04-02 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0011_auto_20180402_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_fname',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_lname',
            field=models.CharField(max_length=80),
        ),
    ]
