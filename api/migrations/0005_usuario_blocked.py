# Generated by Django 4.2.6 on 2024-03-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_sala_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
