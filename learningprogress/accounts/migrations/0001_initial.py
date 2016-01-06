# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    verbose_name='superuser status',
                    default=False)),
                ('username', models.CharField(
                    unique=True,
                    help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
                    max_length=30,
                    validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')],
                    verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='email address')),
                ('is_staff', models.BooleanField(
                    help_text='Designates whether the user can log into this admin site.',
                    verbose_name='staff status',
                    default=False)),
                ('is_active', models.BooleanField(
                    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                    verbose_name='active',
                    default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('exam', models.PositiveIntegerField(
                    help_text='An integer with five digets. The first four digets represent the year, the last diget (1 or 2) represents the season.',
                    null=True,
                    verbose_name='Exam')),
                ('groups', models.ManyToManyField(
                    to='auth.Group',
                    related_query_name='user',
                    help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.',
                    blank=True,
                    verbose_name='groups',
                    related_name='user_set')),
                ('user_permissions', models.ManyToManyField(
                    to='auth.Permission',
                    related_query_name='user',
                    help_text='Specific permissions for this user.',
                    blank=True,
                    verbose_name='user permissions',
                    related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExamDate',
            fields=[
                ('key', models.PositiveIntegerField(
                    help_text='An integer with five digets. The first four digets represent the year, the last diget (1 or 2) represents the season.',
                    primary_key=True,
                    verbose_name='Exam key',
                    serialize=False)),
                ('date', models.DateField(help_text='Choose the first date of the respective exam session.', verbose_name='Date')),
            ],
            options={
                'verbose_name_plural': 'Dates of exam',
                'verbose_name': 'Date of exam',
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
    ]
