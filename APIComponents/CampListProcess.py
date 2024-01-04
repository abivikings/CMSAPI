from django.contrib.auth.models import User, Group
from base.models import *
from django.db import connection
from camp.models import *


class CampList:
    @classmethod
    def camp_total(cls):
        teachers = 0
        students = 0
        parents = 0
        users = 0
        for camp in Camp.objects.exclude(schema_name='public').values():
            connection.set_schema(camp['schema_name'], True)
            teachers = teachers + Teacher.objects.all().values().count()
            students = students + Student.objects.all().values().count()
            parents = parents + Parent.objects.all().values().count()
            users = users + User.objects.filter(is_superuser=True).values().count()
            connection.set_schema_to_public()

        x = {
            "admin_user": users,
            "teachers": teachers,
            "students": students,
            "parents": parents
        }
        return x

    @classmethod
    def get_all_camp(cls):
        camp_lists = []
        camps = Camp.objects.exclude(schema_name='public').values()
        for camp in camps:
            connection.set_schema(camp['schema_name'], True)
            teachers = Teacher.objects.all().values().count()
            students = Student.objects.all().values().count()
            parents = Parent.objects.all().values().count()
            user = list(User.objects.filter(is_superuser=True).values())
            camp['camp_name'] = camp.pop('name')
            camp['camp_domain'] = camp.pop('schema_name')
            camp['camp_admin_name'] = user[0]['first_name'] + " " + user[0]['last_name']
            camp['camp_admin_email'] = user[0]['email']
            camp['teachers'] = teachers
            camp['students'] = students
            camp['parents'] = parents
            camp_lists.append(camp)
            connection.set_schema_to_public()
        return camp_lists

    @classmethod
    def get_camp_info(cls, camp_domain):
        camp = list(Camp.objects.filter(schema_name=camp_domain).values())
        connection.set_schema(camp_domain, True)
        teachers = Teacher.objects.all().values().count()
        students = Student.objects.all().values().count()
        parents = Parent.objects.all().values().count()
        user = list(User.objects.filter(is_superuser=True).values())
        camp[0]['camp_name'] = camp[0].pop('name')
        camp[0]['camp_domain'] = camp[0].pop('schema_name')
        camp[0]['camp_admin_name'] = user[0]['first_name'] + " " + user[0]['last_name']
        camp[0]['camp_admin_email'] = user[0]['email']
        camp[0]['teachers'] = teachers
        camp[0]['students'] = students
        camp[0]['parents'] = parents
        connection.set_schema_to_public()
        return camp


