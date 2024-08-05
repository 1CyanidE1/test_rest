from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .models import FoodCategory
from .serializers import FoodListSerializer


class FoodListView(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of food categories with published foods",
        operation_description="Returns a list of food categories with foods that are published. "
                              "Categories without any published foods are excluded.",
        responses={
            200: FoodListSerializer(many=True),
            404: 'Not Found',
            500: 'Internal Server Error'
        }
    )
    def get(self, request, format=None):
        categories = FoodCategory.objects.filter(food__is_publish=True).distinct()
        result = []

        for category in categories:
            foods = category.food.filter(is_publish=True)
            if foods.exists():
                serialized_category = FoodListSerializer(category).data
                serialized_category['foods'] = [
                    food for food in serialized_category['foods'] if food['internal_code'] in foods.values_list('internal_code', flat=True)
                ]
                result.append(serialized_category)

        return Response(result, status=status.HTTP_200_OK)