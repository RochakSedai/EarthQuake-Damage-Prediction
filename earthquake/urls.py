from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('normal-user', views.normalUser, name='normalUser'),
    path('professional-user', views.professionalUser, name='professionalUser'),
    path('addnormalUserData', views.normalUser_data, name='addnormalUserData'),
    path('addprofessionalUserData', views.professionalUser_data, name='addprofessionalUserData')
]