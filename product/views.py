from rest_framework import generics,permissions, status
from rest_framework.response import Response
from product.models import Category, SubCategory, Product
from product.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer,SalesOverviewSerializer
from rest_framework.views import APIView
from django.db.models import Sum, Count
from product.models import Order

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






class SalesOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # অ্যাডমিন হলে সব ডাটা দেখবে, অন্যথায় শুধু নিজের ডাটা
        orders = Order.objects.all() if user.role == 'ADMIN' else Order.objects.filter(employee=user)

        # ডাইনামিক ক্যালকুলেশন
        overview_data = {
            "total_orders": orders.count(),
            "pending_orders": orders.filter(status='PENDING').count(),
            "complete_orders": orders.filter(status='COMPLETE').count(),
            "cancel_orders": orders.filter(status='CANCEL').count(),
            "total_sales": orders.filter(status='COMPLETE').aggregate(Sum('total_price'))['total_price__sum'] or 0,
            "total_commission": orders.filter(status='COMPLETE').aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0,
        }

        serializer = SalesOverviewSerializer(overview_data)
        
        return Response({
            "message": "Fetched sales overview",
            "data": {
                "requests": serializer.data
            }
        })