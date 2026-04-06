from django.shortcuts import get_object_or_404
from django.contrib import admin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, serializers, permissions
from users.models import Designation, User,Team,Notice
from users.permissions import IsSR, IsTL
from users.serializers import DesignationSerializer, NonStaffUserSerializer, UserCreateWithTokenSerializer,CustomTokenObtainPairSerializer,UserSerializer, TeamSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsAdminOrTL, IsTL, IsSR

from utils.response import success_response, error_response

from users.serializers import (
    TeamSerializer,
    TeamDetailSerializer,
    EmployeeSerializer,
    NoticeSerializer
)
# from .permissions import IsAdmin, IsAdminOrTL

class UserRegisterWithTokenView(generics.CreateAPIView):
    serializer_class = UserCreateWithTokenSerializer
    # permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "user": serializer.data,
                "message": "Registration successful! Waiting for admin acceptance. You can login once approved."
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PendingApprovalUserListView(generics.ListAPIView):
    serializer_class = NonStaffUserSerializer
    permission_classes = [IsAuthenticated & IsAdmin]


    def get_queryset(self):
        # Only return users who are not staff and haven't been accepted yet
        return User.objects.filter(is_accepted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Wrapping the data in your custom structure
        return Response({
            "message": "Fetched all requests",
            "data": {
                "requests": serializer.data
            }
        }, status=status.HTTP_200_OK)


# do Approve Users

class ApproveUserView(APIView):
    permission_classes = [IsAuthenticated & IsAdmin]
    def post(self, request, user_id):
        # Get the user to approve from your User model
        user = get_object_or_404(User, id=user_id)

        # Check if the user is already accepted to avoid redundant saves
        if user.is_accepted:
            return Response(
                {"detail": f"User {user.email} is already accepted."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update the specific field you added earlier
        user.is_accepted = True
        user.save()

        return Response(
            {
                "message": "User approved successfully",
                "data": {
                    "email": user.email,
                    "is_accepted": user.is_accepted
                }
            }, 
            status=status.HTTP_200_OK
        )


#users Login 

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [IsAuthenticated & (IsAdmin | IsTL | IsSR)]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # আপনার চাওয়া ফরম্যাট অনুযায়ী রেসপন্স
        return Response({
            "message": "Logged in successful",
            "data": {
                "token": serializer.validated_data['token'],
                "user_info": serializer.validated_data['user_info']
            }
        }, status=status.HTTP_200_OK)

# allready approved users views


class ApprovedEmployeeListView(generics.ListAPIView):
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated & IsAdmin]

    def get_queryset(self):
        # Admin বাদে সব Approved ইউজারদের ফিল্টার করা
        return User.objects.filter(is_accepted=True).exclude(role='admin')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # আপনার কাস্টম ফরম্যাটে রেসপন্স তৈরি করা
        return Response({
            "message": "Fetched all employees",
            "data": {
                "requests": serializer.data
            }
        }, status=status.HTTP_200_OK)



class DesignationListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAdmin]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer






# কাস্টম পারমিশন: শুধু Admin এক্সেস পাবে
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'



class CreateTeamView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated & IsAdmin]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            team = serializer.save()

            # 🔥 Update leader role to TL
            leader = team.leader
            if leader:
                leader.role = 'TL'
                leader.save()

            return success_response(
                "Team created successfully",
                {"requests": serializer.data},   # ✅ wrapped like you want
                201
            )

        return error_response("Validation failed", serializer.errors)


class GetTeamsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated & IsAdmin]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return success_response(
            "Fetched all teams",
            {"requests": serializer.data}
        )




class AddTeamMemberView(APIView):

    permission_classes = [IsAuthenticated & IsAdmin]
    def post(self, request):
        team_id = request.data.get('team_id')
        employee_id = request.data.get('employee_id')

        team = get_object_or_404(Team, id=team_id)
        employee = get_object_or_404(User, id=employee_id)

        if employee == team.leader:
            return error_response("Leader cannot be a member")

        if team.members.filter(id=employee.id).exists():
            return error_response("Already a member")

        team.members.add(employee)

        return success_response("Member added successfully")
    



class TeamDetailsView(APIView):

    permission_classes = [IsAuthenticated & IsAdmin]

    def get(self, request):
        team_id = request.query_params.get('team_id')
        team = get_object_or_404(Team, id=team_id)

        serializer = TeamDetailSerializer(team)

        return success_response(
            "Team details fetched",
            serializer.data
        )
    


class EmployeeInfoView(APIView):

    permission_classes = [IsAuthenticated & IsAdminOrTL]

    def get(self, request):
        employee_id = request.query_params.get('employee_id')
        employee = get_object_or_404(User, id=employee_id)

        serializer = EmployeeSerializer(employee)

        return success_response(
            "Employee info fetched",
            serializer.data
        )
    

# class CreateNoticeView(APIView):
#     # permission_classes = [IsAuthenticated] # নিশ্চিত করুন ইউজার লগইন করা আছে

#     def post(self, request):
#         serializer = NoticeSerializer(data=request.data)

#         if serializer.is_valid():
#             # সমস্যা এখানে হতে পারে যদি request.user না থাকে
#             # তাই আগে চেক করে নিন ইউজার অথেনটিকেটেড কি না
#             if request.user.is_authenticated:
#                 serializer.save(created_by=request.user)
#                 return Response({
#                     "message": "Notice created successfully",
#                     "data": {"requests": serializer.data}
#                 }, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response({
#             "message": "Validation error",
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)


class CreateNoticeView(APIView):
    # এই পারমিশনটি থাকলে টোকেন ছাড়া কেউ রিকোয়েস্ট পাঠাতে পারবে না
    permission_classes = [IsAuthenticated & IsAdmin]

    def post(self, request):
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid():
            # টোকেন থেকে পাওয়া ইউজারকে 'created_by' হিসেবে সেভ করা হচ্ছে
            serializer.save(created_by=request.user)
            return Response({
                "message": "Notice created successfully",
                "data": {"requests": serializer.data}
            }, status=201)
        
        return Response(serializer.errors, status=400)


class GetNoticeView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_staff:
            notices = Notice.objects.all()
        else:
            notices = Notice.objects.filter(
                teams__in=user.teams_as_member.all()
            ).distinct()

        serializer = NoticeSerializer(notices, many=True)

        return success_response(
            "Notices fetched successfully",
            {"requests": serializer.data}
        )
    





###############################################################
