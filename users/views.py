from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from users.models import Designation, User
from users.serializers import DesignationSerializer, NonStaffUserSerializer, UserCreateWithTokenSerializer,CustomTokenObtainPairSerializer


class UserRegisterWithTokenView(generics.CreateAPIView):
    serializer_class = UserCreateWithTokenSerializer


class DesignationListCreateView(generics.ListCreateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class NonStaffUserListView(generics.ListAPIView):
    serializer_class = NonStaffUserSerializer

    def get_queryset(self):
        # Return only users where is_staff=False
        return User.objects.filter(is_staff=False)


class ApproveUserView(APIView):
    def post(self, request, user_id):
        # Get the user to approve
        user = get_object_or_404(User, id=user_id)
        if user.is_staff:
            return Response({"detail": "User is already approved."}, status=status.HTTP_400_BAD_REQUEST)

        # Approve user
        user.is_staff = True
        user.save()
        return Response({"detail": f"User {user.email} has been approved."}, status=status.HTTP_200_OK)
    


#users Login 
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



###############################################################
from rest_framework import generics, permissions
from users.models import Store, Product, Order
from users.serializers import StoreSerializer, ProductSerializer, OrderSerializer

class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            # এখানে হয় এরর থ্রো করুন অথবা ডিফল্ট কোনো ইউজার দিন
            raise serializers.ValidationError("স্টোর তৈরি করতে লগইন করা আবশ্যক।")

class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        store_id = self.request.query_params.get('store_id')
        if store_id:
            return Product.objects.filter(store_id=store_id)
        return Product.objects.all()

class OrderCreateListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]