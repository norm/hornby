from django.core.management.base import BaseCommand

from tracks.models import TrackUpdate


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'user',
            help="Load USER's scrobbles from last.fm"
        )

    def handle(self, *args, **options):
        TrackUpdate.create_from_lastfm(options['user'])
