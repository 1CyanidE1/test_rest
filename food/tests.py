# menu/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FoodCategory, Food
from .factories import FoodCategoryFactory, FoodFactory


class FoodAPITests(APITestCase):

    def setUp(self):
        self.category = FoodCategoryFactory(name_ru='Напитки')
        self.food1 = FoodFactory(category=self.category, is_publish=True, name_ru='Чай', cost='123.00')
        self.food2 = FoodFactory(category=self.category, is_publish=True, name_ru='Кола', cost='123.00')
        self.food3 = FoodFactory(category=self.category, is_publish=False, name_ru='Непубликованный', cost='123.00')

        self.category2 = FoodCategoryFactory(name_ru='Выпечка')
        self.food4 = FoodFactory(category=self.category2, is_publish=True, name_ru='Булочка', cost='50.00')

    def test_get_food_categories(self):
        url = reverse('food-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        category_names = [category['name_ru'] for category in response.data]
        self.assertIn('Напитки', category_names)
        self.assertIn('Выпечка', category_names)

        for category in response.data:
            if category['name_ru'] == 'Напитки':
                self.assertEqual(len(category['foods']), 2)

    def test_exclude_unpublished_foods(self):
        url = reverse('food-list')
        response = self.client.get(url, format='json')

        for category in response.data:
            for food in category['foods']:
                db_food = Food.objects.get(internal_code=food['internal_code'])
                self.assertTrue(db_food.is_publish)

    def test_exclude_empty_categories(self):
        empty_category = FoodCategoryFactory(name_ru='Пустая категория')
        FoodFactory(category=empty_category, is_publish=False)

        url = reverse('food-list')
        response = self.client.get(url, format='json')

        category_names = [category['name_ru'] for category in response.data]
        self.assertNotIn('Пустая категория', category_names)
