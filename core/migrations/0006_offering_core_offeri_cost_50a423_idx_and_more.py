# Generated by Django 5.1 on 2024-11-30 22:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_statistics'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='offering',
            index=models.Index(fields=['cost'], name='core_offeri_cost_50a423_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['stars'], name='core_review_stars_e6b5c9_idx'),
        ),
    ]
