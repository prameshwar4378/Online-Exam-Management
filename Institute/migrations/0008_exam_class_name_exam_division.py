# Generated by Django 4.2 on 2023-07-12 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0007_rename_end_date_exam_exam_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='class_name',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th'), ('9th', '9th'), ('10th', '10th')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='division',
            field=models.CharField(choices=[('Azalea', 'Azalea'), ('Zinnia', 'Zinnia'), ('Camelia', 'Camelia')], max_length=10, null=True),
        ),
    ]
