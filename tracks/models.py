from django.db import models

from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import make_aware




from datetime import datetime
import json
import os
import time

import requests

import pprint
pp = pprint.PrettyPrinter().pprint


def generate_update_id(update):
    if update['track_mbid']:
        track_id = update['track_mbid']
    else:
        if update['album_mbid']:
            album_id = update['album_mbid']
        else:
            album_id = slugify(update['album_name'])
        track_id = '%s-%s' % (
            slugify(update['track_name']),
            album_id,
        )
    timestamp = int(update['timestamp'].timestamp())
    return '%s-%s' % (track_id, timestamp)


class TrackUpdate(models.Model):
    id = models.CharField(
        max_length = 64,
        primary_key = True,
    )
    track_mbid = models.CharField(
        max_length = 64,
    )
    track_name = models.CharField(
        max_length = 255,
        blank = True,
        null = True,
    )
    album_mbid = models.CharField(
        max_length = 64,
    )
    album_name = models.CharField(
        max_length = 255,
        blank = True,
        null = True,
    )
    artist_mbid = models.CharField(
        max_length = 64,
    )
    artist_name = models.CharField(
        max_length = 255,
        blank = True,
        null = True,
    )
    played = models.BooleanField()
    timestamp = models.DateTimeField()
    received = models.DateTimeField(
        default = timezone.now,
    )

    @classmethod
    def create_from_lastfm(cls, user):
        page = 1
        while page:
            print('-- page %s' % page)
            tracks = requests.get(
                'https://ws.audioscrobbler.com/2.0/',
                params = {
                    'api_key': os.environ['LASTFM_KEY'],
                    'format': 'json',
                    'limit': 100,
                    'method': 'user.getrecenttracks',
                    'page': page,
                    'user': user,
                }
            ).json()

            if 'error' in tracks:
                # "Most likely the backend service failed. Please try again."
                if tracks['error'] == 8:
                    print('-- error 8, sleeping before retrying')
                    time.sleep(30)
                    continue

                # "Your request is missing a required parameter"
                if tracks['error'] == 6:
                    if page != 1:
                        print('-- error 6, sleeping before retrying')
                        time.sleep(30)
                        continue
                    else:
                        raise KeyError

            if not 'recenttracks' in tracks:
                pp(tracks)
                raise Boom

            if len(tracks['recenttracks']['track']) == 0:
                break

            print('--', tracks['recenttracks']['track'][0]['date']['#text'])

            page += 1
            for track in tracks['recenttracks']['track']:
                timestamp = make_aware(
                    datetime.fromtimestamp(int(track['date']['uts']))
                )
                update = {
                    'track_name': track['name'],
                    'track_mbid': track['mbid'],
                    'album_mbid': track['album']['mbid'],
                    'album_name': track['album']['#text'],
                    'artist_mbid': track['artist']['mbid'],
                    'artist_name': track['artist']['#text'],
                    'timestamp': timestamp,
                    'received': timestamp,
                    'played': True,
                }
                id = generate_update_id(update)

                _, created = cls.objects.update_or_create(
                    id=id,
                    defaults=update,
                )
                if not created:
                    pass
                    # page = 0
                    # break
                else:
                    print('[%s] "%s" by "%s"' % (
                        datetime.fromtimestamp(int(track['date']['uts'])),
                        track['name'],
                        track['artist']['#text'],
                    ))

            time.sleep(1)
