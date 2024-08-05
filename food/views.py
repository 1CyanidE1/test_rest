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
        serializer = FoodListSerializer(categories, many=True)
        filtered_data = [category for category in serializer.data if category['foods']]

        return Response(filtered_data, status=status.HTTP_200_OK)
