# Generated by Django 3.0.1 on 2020-01-31 14:43

from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension

class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_auto_20200131_2127'),
    ]

    operations = [
        UnaccentExtension()
    ]
