from urllib import request
from base.models import *
from django.db import connection
from camp.models import *


class CampList:
    @classmethod
    def get_camp_user(cls):
        camp_lists = []
        camps = Camp.objects.exclude(name='public').values()
        # for camp in camps:
        #     connection.set_schema(camp['name'], True)
        #     teachers = Teacher.objects.all().values()
        #     connection.set_schema_to_public()
        return camps
