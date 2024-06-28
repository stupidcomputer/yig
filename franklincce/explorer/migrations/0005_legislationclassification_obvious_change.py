# Generated by Django 4.2.12 on 2024-06-28 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0004_legislationclassification'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislationclassification',
            name='obvious_change',
            field=models.CharField(default='test', help_text='Name of this classification.', max_length=256),
            preserve_default=False,
        ),
    ]
