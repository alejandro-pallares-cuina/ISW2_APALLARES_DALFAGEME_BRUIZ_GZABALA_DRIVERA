"""Merged migration to resolve conflicting 0003 migrations.

This file was created to resolve the leaf-node conflict between
`0003_destination_image` and `0003_review` so tests and makemigrations
can run without prompting for a manual merge.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0003_destination_image'),
        ('relecloud', '0003_review'),
    ]

    operations = []
