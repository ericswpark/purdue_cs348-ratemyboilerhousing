# Generated by Django 5.1 on 2024-11-30 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_review_created_at_review_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('date', models.DateField(auto_now_add=True, primary_key=True, serialize=False)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('user_count', models.IntegerField(default=0)),
                ('housing_count', models.IntegerField(default=0)),
                ('offering_count', models.IntegerField(default=0)),
                ('review_count', models.IntegerField(default=0)),
                ('offering_cost_avg', models.FloatField(default=0)),
                ('offering_cost_min', models.IntegerField(default=0)),
                ('offering_cost_max', models.IntegerField(default=0)),
                ('review_stars_avg', models.FloatField(default=0)),
                ('review_stars_min', models.IntegerField(default=0)),
                ('review_stars_max', models.IntegerField(default=0)),
            ],
        ),
    ]