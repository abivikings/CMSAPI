from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'camp_users', UserViewSet)
router.register(r'teacher', TeacherViewSet)
router.register(r'parent', ParentViewSet)
router.register(r'student', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login, name='login'),
    path('auth_me/', auth_me, name='auth_me'),
    path('get_camp_user/', get_camp_user, name='get_camp_user')
]
