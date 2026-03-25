from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import Designation
from rest_framework import serializers

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

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
        fields = ['id','first_name', 'last_name', 'email', 'address', 'phone_number', 'designation', 'blood_group']
        read_only_fields = ['is_staff']



class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'emp_designation']


class NonStaffUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'NonStaffUser'
        fields = ['id','first_name', 'last_name', 'email', 'address', 'phone_number', 'designation', 'blood_group']