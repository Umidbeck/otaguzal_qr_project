from django.urls import path
from .views import HomeView, edit_product, delete_product, add_product

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    path('add-product/', add_product, name='add_product'),
]