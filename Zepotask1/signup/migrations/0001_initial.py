# Generated by Django 2.0.3 on 2018-03-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_fname', models.CharField(max_length=200)),
                ('user_lname', models.CharField(max_length=200)),
                ('user_email', models.CharField(max_length=200)),
            ],
        ),
    ]
