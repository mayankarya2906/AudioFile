# import dependencies
from django.db import models
from datetime import datetime
from django_mysql.models import ListCharField
from django.db.models import CharField
import django


class Song(models.Model):
    """ Song model: fields: name_of_song, duration, upload_time"""
    # character limitation of 100
    name_of_song = models.CharField(max_length=100)
    duration = models.IntegerField()
    upload_time = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        verbose_name = "song"
        verbose_name_plural = "songs"
        db_table = 'song'


class Podcast(models.Model):
    """ Podcast model: fields: name_of_podcast, duration, upload_time, host, participants"""
    # character limitation of 100
    name_of_podcast = models.CharField(max_length=100)
    duration = models.IntegerField()
    # upload_time is default now as current datetime
    upload_time = models.DateTimeField(default=django.utils.timezone.now)
    host = models.CharField(max_length=100)
    # participants is optional so make it nullable field
    participants = ListCharField(
        base_field=CharField(max_length=100),
        size=10,
        max_length=(10 * 101),
        null = True # 10 * 100 character nominals, plus commas
    )

    class Meta:
        verbose_name = "podcast"
        verbose_name_plural = "podcasts"
        db_table = 'podcast'


class AudioBook(models.Model):
    """ AudioBook model: fields: title_of_the_audiobook, author_of_audiobook, upload_time, narrator, duration"""
    title_of_the_audiobook = models.CharField(max_length=100)
    author_of_audiobook = models.CharField(max_length=100)
    narrator  = models.CharField(max_length=100)
    duration = models.IntegerField()
    upload_time = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        verbose_name = "audiobook"
        verbose_name_plural = "audiobooks"
        db_table = 'audiobook'
