# Generated by Django 5.0.2 on 2024-06-18 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0003_customuser_user_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='submission_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]
