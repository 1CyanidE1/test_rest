import factory
from .models import FoodCategory, Food
import random


class FoodCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodCategory

    name_ru = factory.Faker('word')
    name_en = factory.Faker('word')
    name_ch = factory.Faker('word')
    order_id = factory.Sequence(lambda n: n)


class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Food

    category = factory.SubFactory(FoodCategoryFactory)
    is_vegan = factory.Faker('boolean')
    is_special = factory.Faker('boolean')
    code = factory.Sequence(lambda n: n + 1)
    internal_code = factory.Sequence(lambda n: n + 100)
    name_ru = factory.Faker('word')
    description_ru = factory.Faker('sentence')
    description_en = factory.Faker('sentence')
    description_ch = factory.Faker('sentence')
    cost = factory.LazyAttribute(lambda _: round(random.uniform(50.0, 500.0), 2))
    is_publish = factory.Faker('boolean')

    @factory.post_generation
    def additional(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for add in extracted:
                self.additional.add(add)
