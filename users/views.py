from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, serializers
from users.models import Designation, User, Store, Product, Order
from users.serializers import DesignationSerializer, NonStaffUserSerializer, UserCreateWithTokenSerializer,CustomTokenObtainPairSerializer, StoreSerializer, ProductSerializer, OrderSerializer


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




class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    # প্রোডাকশনে এটি আন-কমেন্ট করে দিবেন
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # ইউজার লগইন না থাকলে যেন ৫০০ এরর না দিয়ে ৪০০ এরর দেয়
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError({"detail": "স্টোর তৈরি করতে লগইন করা আবশ্যক।"})
        
        serializer.save(owner=self.request.user)

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