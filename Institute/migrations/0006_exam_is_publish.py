# Generated by Django 4.2 on 2023-07-12 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0005_exam_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='is_publish',
            field=models.BooleanField(default=False),
        ),
    ]
