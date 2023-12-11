from django.contrib.auth.models import User
from django.db import connection


class GetUserRole:
    @classmethod
    def get_subdomain(cls, request):
        host = request.get_host()  # Get the host from the request
        host_parts = host.split('.')
        subdomain = host_parts[0]
        return subdomain

    @classmethod
    def get_user_role(cls, email, request):
        subdomain = cls.get_subdomain(request)
        connection.set_schema_to_public()
        user = User.objects.get(email=email)
        role = user.groups.values_list('name', flat=True)[0]
        connection.set_schema(subdomain, True)
        return role
