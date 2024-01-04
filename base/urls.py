from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('super_admin/', super_admin_login, name='super_admin'),
    path('create_camp/', create_camp, name='create_camp'),
    path('auth_me/', auth_me, name='auth_me'),
    path('check_domain/', check_domain, name='check_domain'),
    path('get_auth_group/', get_auth_group, name='get_auth_group'),
    path('get_all_camp_admin/', get_all_camp_admin, name='get_all_camp_admin'),
    path('get_all_camp/', get_all_camp, name='get_all_camp'),
    path('get_camp_details/', get_camp_details, name='get_camp_details'),
    path('camp_total/', camp_total, name='camp_total'),
]
