# Generated by Django 4.2 on 2023-07-16 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0015_exam_exam_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='exam_time',
            new_name='exam_duration',
        ),
    ]
