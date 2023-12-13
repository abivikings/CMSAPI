from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from rest_framework_simplejwt.tokens import RefreshToken

from camp.views import get_user_role
from .models import *
from .utils import generate_access_token, generate_refresh_token
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.url_parser import parse_url

JWT_authenticator = JWTAuthentication()


@api_view(['GET'])
def get_all_camp_admin(request):
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
def get_auth_group(request):
    queryset = Group.objects.all()
    result_list = list(queryset.values())
    return Response(result_list)


@api_view(['POST'])
def check_domain(request):
    is_schema = list(Camp.objects.filter(schema_name=request.data['camp_domain']).values())
    if is_schema:
        return Response(is_schema[0]['schema_name'], status=status.HTTP_200_OK)
    else:
        return Response('Not found any domain', status=status.HTTP_404_NOT_FOUND)


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


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def super_admin_login(request):
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
                        'role': user.groups.values_list('name', flat=True)[0],
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
        return Response(e)
    return Response("Somthing went wrong")


@api_view(['POST'])
def create_camp(request):
    url = request.build_absolute_uri()
    protocol, subdomain, host_name = parse_url(url)
    try:
        tenant = Camp(schema_name=request.data['camp_domain'], name=request.data['camp_name'])
        tenant.save()
        domain = request.data['camp_domain'] + '.' + host_name
        domain = Domain(domain=domain, tenant=tenant, is_primary=True)
        domain.save()
        user = User.objects.create(first_name='Camp',
                                   last_name='Admin',
                                   username=request.data['camp_domain'],
                                   email=request.data['camp_admin_email'],
                                   password=make_password(request.data['password']),
                                   is_superuser=False,
                                   is_staff=True,
                                   is_active=True
                                   )
        group = Group.objects.get(pk=1)
        group.user_set.add(user)

        connection.set_schema(request.data['camp_domain'], True)
        Group.objects.create(name='camp_admin')
        Group.objects.create(name='parent')
        Group.objects.create(name='student')
        Group.objects.create(name='teacher')
        camp_user = User.objects.create(first_name='Camp',
                                        last_name='Admin',
                                        username=request.data['camp_domain'],
                                        email=request.data['camp_admin_email'],
                                        password=make_password(request.data['password']),
                                        is_superuser=True,
                                        is_staff=True,
                                        is_active=True
                                        )
        camp_group = Group.objects.get(pk=1)
        camp_group.user_set.add(camp_user)
        connection.set_schema_to_public()
        return Response({'status': 'Camp Created'})
    except Exception as ex:
        return Response(ex, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return HttpResponse("<h1>Public Index</h1>")
