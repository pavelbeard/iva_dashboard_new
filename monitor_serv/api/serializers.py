from rest_framework import serializers

from dashboard.models import Target, CPU


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('id', 'address', 'port', 'username', 'password', 'is_being_scan')


class CpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
