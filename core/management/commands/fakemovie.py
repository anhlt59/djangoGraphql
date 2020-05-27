from django.core.management import BaseCommand, CommandError
from api.models import Director, Movie
from faker import Faker
from itertools import islice
import random


class Command(BaseCommand):
    help = "fake data"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="number of records")

    def create_bulk_data(self, n):
        fake = Faker(["en-US"])
        directors = list(Director.objects.all())

        for _ in range(n):
            title = fake.paragraph()
            year = fake.year()
            director = random.choice(directors)
            yield Movie(title=title, year=year, director=director)

    def handle(self, *args, **options):
        N = options["number"]
        count = 0

        objs = self.create_bulk_data(N)

        while batch := list(islice(objs, 100)): # batch size = 100
            Movie.objects.bulk_create(batch, ignore_conflicts=True)
            count += len(batch)
            self.stdout.write(f"Bulk created {count} Movie")

        # collect stats
        total = Movie.objects.count()
        self.stdout.write(f"\nTotal: {total}")
