# Generated by Django 4.1.7 on 2024-10-12 03:00

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0002_auto_20200519_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human/computer readable name.', max_length=100, unique=True, verbose_name='Name')),
                ('everyone', models.BooleanField(blank=True, help_text='Flip this flag on (Yes) or off (No) for everyone, overriding all other settings. Leave as Unknown to use normally.', null=True, verbose_name='Everyone')),
                ('percent', models.DecimalField(blank=True, decimal_places=1, help_text='A number between 0.0 and 99.9 to indicate a percentage of users for whom this flag will be active.', max_digits=3, null=True, verbose_name='Percent')),
                ('testing', models.BooleanField(default=False, help_text='Allow this flag to be set for a session for user testing', verbose_name='Testing')),
                ('superusers', models.BooleanField(default=True, help_text='Flag always active for superusers?', verbose_name='Superusers')),
                ('staff', models.BooleanField(default=False, help_text='Flag always active for staff?', verbose_name='Staff')),
                ('authenticated', models.BooleanField(default=False, help_text='Flag always active for authenticated users?', verbose_name='Authenticated')),
                ('languages', models.TextField(blank=True, default='', help_text='Activate this flag for users with one of these languages (comma-separated list)', verbose_name='Languages')),
                ('rollout', models.BooleanField(default=False, help_text='Activate roll-out mode?', verbose_name='Rollout')),
                ('note', models.TextField(blank=True, help_text='Note where this Flag is used.', verbose_name='Note')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text='Date when this Flag was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, help_text='Date when this Flag was last modified.', verbose_name='Modified')),
                ('groups', models.ManyToManyField(blank=True, help_text='Activate this flag for these user groups.', to='auth.group', verbose_name='Groups')),
                ('teams', models.ManyToManyField(blank=True, help_text='Activate this flag for these teams.', to='teams.team')),
                ('users', models.ManyToManyField(blank=True, help_text='Activate this flag for these users.', to=settings.AUTH_USER_MODEL, verbose_name='Users')),
            ],
            options={
                'verbose_name': 'Flag',
                'verbose_name_plural': 'Flags',
                'abstract': False,
            },
        ),
    ]
