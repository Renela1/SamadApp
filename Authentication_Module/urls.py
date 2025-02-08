from django.urls import path

from . import views

urlpatterns = [
    path('student-login/', views.StudentsLogin.as_view(), name='student_login_page'),
    path('staff-login/', views.StaffLogin.as_view(), name='staff_login_page'),
    path('add-student/', views.AddStudentView.as_view(), name='add_student_page'),
    path('add-staff/', views.AddStaffView.as_view(), name='add_staff_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_account'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
]
