# Generated by Django 2.0.3 on 2018-04-03 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0012_auto_20180402_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_verf_link',
            field=models.CharField(default='null', max_length=100),
        ),
    ]
