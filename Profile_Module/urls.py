from django.urls import path
from . import views

urlpatterns = [
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('profile', views.profile_view, name='profile'),
    path('edit-info', views.edit_personal_info, name='edit-info'),
    path('pfp', views.change_pfp, name='pfp'),
    path('contacts/reply/<str:first_name>-<str:last_name>/', views.reply_contact, name='reply_contact'),
    path('inbox/', views.inbox_user, name='inbox'),
    path('contacts/', views.all_contacts, name='all_contacts'),
    path('send-notifications/<str:role>/', views.send_notification, name='send_notification'),
    path('notifications/', views.show_notifications, name='show_notifications'),
    path('show-contacts/', views.show_contacts, name='show_contacts')
]
