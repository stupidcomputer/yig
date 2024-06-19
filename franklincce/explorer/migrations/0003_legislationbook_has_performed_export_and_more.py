# Generated by Django 4.2.12 on 2024-06-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0002_legislativetext_legislation_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislationbook',
            name='has_performed_export',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='legislationbook',
            name='import_strategy',
            field=models.CharField(choices=[('HSYIGBookParser', 'High School YIG Book Parser 1'), ('HSMUNBookParser', 'High School MUN Book Parser 1')], default='HSYIGBookParser', max_length=128),
        ),
    ]
