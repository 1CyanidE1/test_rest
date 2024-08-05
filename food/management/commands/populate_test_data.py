from django.core.management.base import BaseCommand
from food.factories import FoodCategoryFactory, FoodFactory


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        categories = FoodCategoryFactory.create_batch(5)
        for category in categories:
            FoodFactory.create_batch(10, category=category)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data'))
