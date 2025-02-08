from django.urls import path

from . import views

urlpatterns = [
    path('contact-us/', views.ContactView.as_view(), name='contact_us_page'),
]
