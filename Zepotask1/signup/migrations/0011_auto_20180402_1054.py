# Generated by Django 2.0.3 on 2018-04-02 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0010_auto_20180402_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
