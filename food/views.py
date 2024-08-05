from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FoodCategory
from .serializers import FoodListSerializer

class FoodListView(APIView):
    def get(self, request, format=None):
        categories = FoodCategory.objects.filter(food__is_publish=True).distinct()
        serializer = FoodListSerializer(categories, many=True)
        filtered_data = [category for category in serializer.data if category['foods']]

        return Response(filtered_data, status=status.HTTP_200_OK)
