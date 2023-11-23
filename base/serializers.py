from rest_framework import serializers
from .models import Camp


class CampSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Camp
        fields = '__all__'
