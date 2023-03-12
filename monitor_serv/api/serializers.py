from rest_framework import serializers

from dashboard.models import Target, PromQL, BackendSettings


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('id', 'address', 'port')


class PromQLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromQL
        fields = ('id', 'query')


class BackendSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackendSettings
        fields = ('refresh_interval', )
