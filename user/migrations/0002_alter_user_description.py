# Generated by Django 3.2.9 on 2021-12-13 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(default='salut ! jutilise HolaApp', max_length=100),
        ),
    ]