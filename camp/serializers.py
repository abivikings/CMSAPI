from rest_framework import serializers
from django.contrib.auth.models import User, Group
from APIComponents.GetUserRole import GetUserRole as UserRole
from .models import *


class UserSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'group_id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group_id = validated_data.pop('group_id', None)
        user = User.objects.create_user(**validated_data)
        if group_id:
            group = UserRole.get_user_role(user.email, self.context.get('request'))
            group.user_set.add(user)
        return user

    def update(self, instance, validated_data):
        group_id = validated_data.pop('group_id', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()

        if group_id:
            instance.groups.clear()
            group = Group.objects.get(pk=group_id)
            instance.groups.add(group)

        return instance


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    parent = Parent.objects.all()
    class Meta:
        model = Student
        fields = '__all__'
