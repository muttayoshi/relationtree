# Generated by Django 3.2.16 on 2023-01-23 18:38

import app.locations.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=254, null=True)),
                ('created_by', models.CharField(blank=True, max_length=254, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(max_length=500)),
                ('postal_code', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=254, null=True)),
                ('created_by', models.CharField(blank=True, max_length=254, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(max_length=50)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=3, null=True, validators=[app.locations.models.validate_minimum])),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=254, null=True)),
                ('created_by', models.CharField(blank=True, max_length=254, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(max_length=50)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'districts',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=254, null=True)),
                ('created_by', models.CharField(blank=True, max_length=254, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(max_length=50)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'provinces',
            },
        ),
        migrations.CreateModel(
            name='SubDistrict',
            fields=[
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=254, null=True)),
                ('created_by', models.CharField(blank=True, max_length=254, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(max_length=50)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'sub_districts',
            },
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='location',
            name='country',
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'countries'},
        ),
        migrations.RemoveField(
            model_name='country',
            name='country_code',
        ),
        migrations.AddField(
            model_name='country',
            name='meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
