# Generated by Django 3.2.16 on 2022-12-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0011_remove_user_detail_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_detail',
            name='number',
            field=models.CharField(max_length=10, null=True),
        ),
    ]