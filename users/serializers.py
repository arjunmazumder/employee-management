from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from users.models import User

from users.models import Designation
from rest_framework import serializers

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import Team,Team, Notice







class UserCreateWithTokenSerializer(BaseUserCreateSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'name', 'email', 'password', 'confirm_password', 
                  'address', 'phone_number', 'role', 'blood_group', 'is_accepted']
        read_only_fields = ['is_accepted'] # Users cannot accept themselves

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password and confirm password do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        # is_accepted will be False by default from the model
        return User.objects.create_user(**validated_data)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id','name', 'email', 'address', 'phone_number', 'role', 'blood_group']
        read_only_fields = ['is_staff']



class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'emp_designation']


class NonStaffUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'NonStaffUser'
        fields = ['id','name', 'email', 'address', 'phone_number', 'role', 'blood_group']


#Login serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # ইমেল এবং পাসওয়ার্ড চেক
        data = super().validate(attrs)

        # ইউজার অনুমোদিত কি না চেক
        if not self.user.is_accepted:
            raise serializers.ValidationError(
                {"detail": "Your account is pending approval. Please contact the administrator."}
            )

        # ইউজার ইনফরমেশন সেট করা
        user_info = {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email,
            'address': self.user.address,
            'phone_number': self.user.phone_number,
            'role': self.user.role,  # এখন ফ্রন্টএন্ড জানবে সে Admin না কি SR
            'blood_group': self.user.blood_group,
            # 'designation': self.user.designation,
            'is_accepted': self.user.is_accepted,
        }
        
        # মূল টোকেন এবং ইউজার ইনফো রিটার্ন করা
        return {
            "token": data, # এতে access এবং refresh দুইটাই থাকবে
            "user_info": user_info
        }
    



class TeamSerializer(serializers.ModelSerializer):
    leader_name = serializers.ReadOnlyField(source='leader.email')

    class Meta:
        model = Team
        fields = ['id', 'team_name', 'leader', 'leader_name', 'members']


class TeamDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'team_name', 'leader', 'members']

    def get_members(self, obj):
        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in obj.members.all()
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'phone_number', 'address']


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'image', 'teams']







######################################################