# Generated by Django 4.2.7 on 2023-12-05 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='users/image/anonim.jpg', upload_to='users/image/'),
        ),
    ]
