# Generated by Django 4.2.6 on 2024-03-22 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_usuario_blocked'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
