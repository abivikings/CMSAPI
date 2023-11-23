from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('super_admin/', super_admin_login, name='super_admin'),
    path('create_camp/', create_camp, name='create_camp'),
    path('auth_me/', auth_me, name='auth_me'),
    path('check_domain/', check_domain, name='check_domain'),
    path('get_auth_group/', get_auth_group, name='get_auth_group'),
]
