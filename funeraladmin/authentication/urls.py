from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import LoginView,LogoutView,RegisterStaffView,StaffMembersView,EmployeeProfile,DeleteEmployee

urlpatterns = [
    path('', StaffMembersView.as_view(), name="staff-members"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', login_required(LogoutView.as_view(),login_url='/auth/login/'), name="logout"),
    path('register-staff/', RegisterStaffView.as_view(), name="add-staff"),
    path('staff-profile/?P<id>[0-9]+)\\Z', EmployeeProfile.as_view(), name="employee-profile"),
    path('delete-staff/?P<id>[0-9]+)\\Z', DeleteEmployee.as_view(), name="delete-employee"),

]
