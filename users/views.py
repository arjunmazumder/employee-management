from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics
from users.models import Designation, User
from users.serializers import DesignationSerializer, NonStaffUserSerializer

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