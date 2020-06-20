from django.core.management.base import BaseCommand

from tracks.models import TrackUpdate


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'user',
            help="Load USER's scrobbles from last.fm"
        )
        parser.add_argument(
            '--full',
            action='store_true',
            help=(
                'Keep trying to load more scrobbles, even once duplciates '
                'start to be found. Most useful when the initial load '
                'failed or was interrupted.'
            )
        )

    def handle(self, *args, **options):
        TrackUpdate.create_from_lastfm(options['user'])
