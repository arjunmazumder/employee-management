from django.urls import path
from users.views import DesignationListCreateView, NonStaffUserListView, ApproveUserView,  UserRegisterWithTokenView, CustomTokenObtainPairView

from users.views import StoreListCreateView, InventoryListCreateView, OrderRetrieveUpdateDeleteView




urlpatterns = [
    path('users-register/', UserRegisterWithTokenView.as_view(), name='register-token'),
    path('designations/', DesignationListCreateView.as_view(), name='designation-list-create'),
    path('non-staff-users/', NonStaffUserListView.as_view(), name='non-staff-users'),
    path('approve-user/<int:user_id>/', ApproveUserView.as_view(), name='approve-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    ######################################################################################
    path('stores/', StoreListCreateView.as_view(), name='store-list-create'),
    path('inventory/', InventoryListCreateView.as_view(), name='inventory-list-create'),
    # path('orders/', OrderCreateListView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDeleteView.as_view(), name='order-detail'),
]