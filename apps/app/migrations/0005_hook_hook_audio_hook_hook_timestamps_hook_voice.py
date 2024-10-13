# Generated by Django 4.1.7 on 2024-10-13 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_textcontentsimilarity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hook',
            name='hook_audio',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='hook',
            name='hook_timestamps',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hook',
            name='voice',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
