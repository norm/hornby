# Generated by Django 3.0.7 on 2020-06-19 14:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackUpdate',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('track_mbid', models.CharField(max_length=64)),
                ('track_name', models.CharField(blank=True, max_length=255, null=True)),
                ('album_mbid', models.CharField(max_length=64)),
                ('album_name', models.CharField(blank=True, max_length=255, null=True)),
                ('artist_mbid', models.CharField(max_length=64)),
                ('artist_name', models.CharField(blank=True, max_length=255, null=True)),
                ('played', models.BooleanField()),
                ('timestamp', models.DateTimeField()),
                ('received', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]