from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "This commands tells me I love you"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want to me to tell you I love you",
        )

    def handle(self, *arg, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            # self.stdout.write(self.style.WARNING("I love you"))
            # self.stdout.write(self.style.ERROR("I love you"))
            self.stdout.write(self.style.SUCCESS("I love you"))

