# Generated by Django 4.2 on 2023-07-12 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0006_exam_is_publish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='end_date',
            new_name='exam_date',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='start_date',
        ),
    ]
