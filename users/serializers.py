from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import Designation
from rest_framework import serializers

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    # Add confirm_password field
    confirm_password = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 
                  'confirm_password', 'address', 'phone_number', 'designation', 'blood_group']

    def validate(self, attrs):
        # Check if password and confirm_password match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password and confirm password do not match."})
        return attrs

    def create(self, validated_data):
        # Remove confirm_password before creating user
        validated_data.pop('confirm_password', None)
        return super().create(validated_data)

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