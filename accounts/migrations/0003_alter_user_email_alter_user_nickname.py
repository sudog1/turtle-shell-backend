# Generated by Django 4.2.5 on 2023-10-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=128, null=True, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='nickname'),
        ),
    ]
