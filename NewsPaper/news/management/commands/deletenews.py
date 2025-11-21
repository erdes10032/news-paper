from django.core.management.base import BaseCommand, CommandError
from ...models import Post


class Command(BaseCommand):
    help = 'Delete news'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all news? yes/no')
        answer = input()

        if answer == 'yes':
            Post.objects.filter(post_type='news').delete()
            self.stdout.write(self.style.SUCCESS('Succesfully deleted news!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))