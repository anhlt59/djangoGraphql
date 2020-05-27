from django.core.management import BaseCommand, CommandError
from api.models import Director
from itertools import islice
from faker import Faker


class Command(BaseCommand):
    help = "fake data"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="number of records", default=1)

    def create_bulk_data(self, n):
        fake = Faker(["en-US"])

        for _ in range(n):
            name = fake.first_name()
            surname = fake.last_name()
            yield Director(name=name, surname=surname)

    def handle(self, *args, **options):
        N = options["number"]
        count = 0

        objs = self.create_bulk_data(N)

        while batch := list(islice(objs, 100)): # batch size = 100
            Director.objects.bulk_create(batch, ignore_conflicts=True)
            count += len(batch)
            self.stdout.write(f"Bulk created {count} Director")

        # collect stats
        total = Director.objects.count()
        self.stdout.write(f"\nTotal: {total}")
