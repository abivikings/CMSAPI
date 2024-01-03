from urllib import request
from base.models import *
from django.db import connection
from camp.models import *


class CampList:
    @classmethod
    def get_camp_user(cls):
        camp_lists = []
        camps = Camp.objects.exclude(schema_name='public').values()
        for camp in camps:
            connection.set_schema(camp['schema_name'], True)
            teachers = Teacher.objects.all().values()
            students = Student.objects.all().values()
            parents = Parent.objects.all().values()
            camp['teachers'] = list(teachers)
            camp['students'] = list(students)
            camp['parents'] = list(parents)
            camp_lists.append(camp)
            connection.set_schema_to_public()
        return camp_lists
