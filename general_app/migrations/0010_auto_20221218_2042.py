# Generated by Django 3.2.16 on 2022-12-18 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0009_auto_20221218_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificatefile',
            name='is_upload',
        ),
        migrations.AddField(
            model_name='user_detail',
            name='is_upload',
            field=models.BooleanField(default=0),
        ),
    ]
