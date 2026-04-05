from rest_framework import generics, status
from rest_framework.response import Response
from product.models import Category, SubCategory, Product
from product.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer

# --- POST Methods (Admin) ---
class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer

class CreateSubCategoryView(generics.CreateAPIView):
    serializer_class = SubCategorySerializer

class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer

# --- GET Methods (Employee/Admin) ---
class GetCategoriesView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GetSubCategoriesView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    
    def get_queryset(self):
        # অপশনাল: নির্দিষ্ট ক্যাটাগরির সাব-ক্যাটাগরি পেতে ফিল্টার
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return SubCategory.objects.filter(category_id=category_id)
        return SubCategory.objects.all()


class GetProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        cat_id = self.request.query_params.get('category_id')
        sub_cat_id = self.request.query_params.get('subcategory_id')
        
        if cat_id:
            queryset = queryset.filter(category_id=cat_id)
        if sub_cat_id:
            queryset = queryset.filter(subcategory_id=sub_cat_id)
        return queryset
