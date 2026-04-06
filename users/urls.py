from django.urls import path
from users.views import (DesignationListCreateView, PendingApprovalUserListView, ApproveUserView,  
                         UserRegisterWithTokenView, CustomTokenObtainPairView,ApprovedEmployeeListView, 
                         CreateTeamView,GetTeamsView, AddTeamMemberView,TeamDetailsView,
                         EmployeeInfoView,CreateNoticeView,GetNoticeView

                        )




urlpatterns = [
    path('registration/', UserRegisterWithTokenView.as_view(), name='register-token'),
    path('designations/', DesignationListCreateView.as_view(), name='designation-list-create'),
    path('requestList/', PendingApprovalUserListView.as_view(), name='non-staff-users'),
    path('acceptRegistration/<int:user_id>/', ApproveUserView.as_view(), name='approve-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get_employees/', ApprovedEmployeeListView.as_view(), name='approved-employee-list'),

    path('create_team/', CreateTeamView.as_view()),
    path('get_teams/', GetTeamsView.as_view()),
    path('add_team_member/', AddTeamMemberView.as_view()),
    path('team_details/', TeamDetailsView.as_view()),
    path('get_employee_info/', EmployeeInfoView.as_view()),
    path('create_notice/', CreateNoticeView.as_view()),
    path('get_notice/', GetNoticeView.as_view()),


]