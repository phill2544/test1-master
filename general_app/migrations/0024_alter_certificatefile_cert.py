# Generated by Django 3.2.16 on 2022-12-01 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0023_alter_certificatefile_cert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatefile',
            name='cert',
            field=models.FileField(upload_to='Document/%Y'),
        ),
    ]