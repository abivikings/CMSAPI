from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('auth_me/', auth_me, name='auth_me'),
    path('get_camp_user/', get_camp_user, name='get_camp_user')
]
