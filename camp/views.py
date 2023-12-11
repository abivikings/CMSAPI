from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from base.utils import generate_access_token, generate_refresh_token
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import connection

from camp.serializers import UserSerializer

JWT_authenticator = JWTAuthentication()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_camp_user(request):
    users = list(User.objects.all().values())
    for user in users:
        user['avatar'] = ''
        user['role'] = 'super_admin'
    user = {
        'allData': users,
        'users': users,
        'params': '',
        'total': 1
    }
    return Response(user)


@api_view(['GET'])
def auth_me(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        # unpacking
        user, token = response
        user = User.objects.get(username=user)
        userData = {
            'userData': {
                'userId': user.email,
                'username': user.username,
                'Id': user.id,
                'email': user.email,
                'role': get_user_role(user.email, request),
                'IsActive': user.is_active,
                'EntryDt': user.date_joined
            }
        }
        return Response(userData, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_auth_group(request):
    queryset = Group.objects.all()
    result_list = list(queryset.values())
    return Response(result_list)


def get_subdomain(request):
    host = request.get_host()  # Get the host from the request
    host_parts = host.split('.')
    subdomain = host_parts[0]

    return subdomain


def get_user_role(email, request):
    subdomain = get_subdomain(request)
    connection.set_schema_to_public()
    user = User.objects.get(email=email)
    role = user.groups.values_list('name', flat=True)[0]
    connection.set_schema(subdomain, True)
    return role


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login(request):
    if not request.data:
        return Response({'error': "Please provide username/password"}, status="400")

    email = request.data['email']
    response = Response()
    try:
        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        if user.check_password(request.data['password']):
            if user:
                access_token, expire_date = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                response.set_cookie(key='Authorization', value=refresh_token)
                response.data = {
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                    'expiration': expire_date,
                    'userData': {
                        'userId': user.email,
                        'username': user.username,
                        'Id': user.id,
                        'email': user.email,
                        'role': get_user_role(user.email, request),
                        'IsActive': user.is_active,
                        'EntryDt': user.date_joined
                    }
                }

                return response
            else:
                return Response(
                    {'Error': "Invalid credentials"},
                    status=400,
                    content_type="application/json"
                )
    except Exception as e:
        return Response()
    return Response({"Somthing went wrong"})
