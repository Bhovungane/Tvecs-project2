from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'This command has been deleted as per user request.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('This command has been deleted and is no longer available.'))
