# Generated by Django 3.2.16 on 2022-12-02 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0025_configuration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='sent_mail_date',
            new_name='send_mail_date',
        ),
    ]
