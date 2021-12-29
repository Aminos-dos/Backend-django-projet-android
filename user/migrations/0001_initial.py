# Generated by Django 2.2.24 on 2021-11-30 20:15

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(default='utilisateur HolaApp', max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('photo', models.ImageField(default='default.jpg', upload_to=user.models.User.get_profile_image)),
                ('phone', models.CharField(max_length=12)),
                ('gender', models.CharField(choices=[('M', 'Men'), ('F', 'Female')], default='M', max_length=5)),
                ('email', models.EmailField(max_length=100, unique=True)),
            ],
        ),
    ]