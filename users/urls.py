from django.urls import path, include
from users.views import DesignationListCreateView, NonStaffUserListView, ApproveUserView

urlpatterns = [
    path('designations/', DesignationListCreateView.as_view(), name='designation-list-create'),
    path('non-staff-users/', NonStaffUserListView.as_view(), name='non-staff-users'),
    path('approve-user/<int:user_id>/', ApproveUserView.as_view(), name='approve-user'),
]