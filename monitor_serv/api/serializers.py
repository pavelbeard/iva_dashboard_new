from rest_framework import serializers

from dashboard.models import Target, CPU


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('id', 'address', 'port',)


class CpuDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = ('metrics', 'record_date')
