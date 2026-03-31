from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from users.models import User, Store, Product, Order, OrderItem

from users.models import Designation
from rest_framework import serializers

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class UserCreateWithTokenSerializer(BaseUserCreateSerializer):
    confirm_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)  # Add token field

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'name', 'email', 'password', 
                  'confirm_password', 'address', 'phone_number', 'designation', 'blood_group', 'token']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password and confirm password do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove confirm_password
        user = super().create(validated_data)
        return user

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id','name', 'email', 'address', 'phone_number', 'designation', 'blood_group']
        read_only_fields = ['is_staff']



class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'emp_designation']


class NonStaffUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'NonStaffUser'
        fields = ['id','name', 'email', 'address', 'phone_number', 'designation', 'blood_group']


#Login serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # প্রথমে ইমেল এবং পাসওয়ার্ড ঠিক আছে কি না তা ডিফল্ট ভাবে চেক হবে
        data = super().validate(attrs)

        # ইউজার যদি অনুমোদিত (is_staff=True) না হয়, তবে লগইন করতে দিবে না
        if not self.user.is_staff:
            raise serializers.ValidationError(
                {"detail": "Your account is pending approval. Please contact the administrator."}
            )

        # ইউজার অনুমোদিত হলে নিচের তথ্যগুলো রিটার্ন করবে
        data['user'] = {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email,
            'address': self.user.address,
            'phone_number': self.user.phone_number,
            'blood_group': self.user.blood_group,
            'designation': self.user.designation,
            'is_staff': self.user.is_staff,
        }
        return data
    

######################################################


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['owner']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'store', 'customer_email', 'total_amount', 'status', 'items', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order