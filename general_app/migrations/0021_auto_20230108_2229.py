# Generated by Django 3.2.16 on 2023-01-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0020_verify_certificatefile_user_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verify_certificatefile',
            name='editing_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='verify_certificatefile',
            name='user_create',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
