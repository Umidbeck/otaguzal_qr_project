from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_uz', 'name_ru')  # Ro‘yxatda ko‘rsatiladigan maydonlar
    search_fields = ('name_en', 'name_uz', 'name_ru')  # Qidiruv maydonlari

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_uz', 'name_ru', 'price', 'discount_percentage', 'category')  # Ro‘yxatda ko‘rsatiladigan maydonlar
    list_filter = ('category', 'discount_percentage')  # Filtrlash uchun maydonlar
    search_fields = ('name_en', 'name_uz', 'name_ru', 'description_en', 'description_uz', 'description_ru')  # Qidiruv maydonlari
    list_editable = ('price', 'discount_percentage')  # To‘g‘ridan-to‘g‘ri tahrirlanadigan maydonlar', 'name_uz', 'name_ru')