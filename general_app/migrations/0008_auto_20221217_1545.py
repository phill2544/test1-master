# Generated by Django 3.2.16 on 2022-12-17 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0007_user_detail_is_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_detail',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user_detail',
            name='position',
            field=models.CharField(max_length=50, null=True),
        ),
    ]