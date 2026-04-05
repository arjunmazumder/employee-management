from django.urls import path
from .views import *

urlpatterns = [
    # Create APIs
    path('create_category/', CreateCategoryView.as_view(), name='create-category'),
    path('create_subcategory/', CreateSubCategoryView.as_view(), name='create-subcategory'),
    path('create_products/', CreateProductView.as_view(), name='create-product'),

    # Get APIs
    path('get_categories/', GetCategoriesView.as_view(), name='get-categories'),
    path('get_subcategories/', GetSubCategoriesView.as_view(), name='get-subcategories'),
    path('get_products/', GetProductsView.as_view(), name='get-products'),
]