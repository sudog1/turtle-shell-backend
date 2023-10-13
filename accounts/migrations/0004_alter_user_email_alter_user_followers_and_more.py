# Generated by Django 4.2.5 on 2023-10-11 19:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('accounts', '0003_alter_user_email_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='admin@naver.com', max_length=128, unique=True, verbose_name='email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='followees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='Admin', max_length=32, unique=True, verbose_name='nickname'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='styles',
            field=models.ManyToManyField(related_name='users', to='articles.style'),
        ),
    ]
