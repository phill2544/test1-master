# Generated by Django 3.2.16 on 2022-12-11 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0003_auto_20221209_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='delete_date_status',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='sender_mail_status',
            field=models.BooleanField(default=0),
        ),
    ]
