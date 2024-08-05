from django.contrib import admin
from .models import FoodCategory, Food


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_en', 'name_ch', 'order_id')
    search_fields = ('name_ru', 'name_en', 'name_ch')
    list_filter = ('order_id',)
    ordering = ('order_id', 'name_ru')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'category', 'is_publish', 'is_vegan', 'is_special', 'cost')
    search_fields = ('name_ru', 'description_ru')
    list_filter = ('category', 'is_vegan', 'is_special', 'is_publish')
    ordering = ('category', 'name_ru')
    autocomplete_fields = ('additional',)
