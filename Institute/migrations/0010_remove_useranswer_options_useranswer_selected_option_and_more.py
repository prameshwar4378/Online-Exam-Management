# Generated by Django 4.2 on 2023-07-14 00:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0009_useranswer_delete_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='options',
        ),
        migrations.AddField(
            model_name='useranswer',
            name='selected_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.option'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.question'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
