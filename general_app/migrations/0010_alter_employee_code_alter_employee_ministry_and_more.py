# Generated by Django 4.1.1 on 2022-11-23 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0009_alter_employee_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='code',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='employee',
            name='ministry',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='employee',
            name='province',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]