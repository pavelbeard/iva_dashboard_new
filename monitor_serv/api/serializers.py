from rest_framework import serializers

from dashboard.models import Target, PromQL, DashboardSettings


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('id', 'address', 'port')


class PromQLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromQL
        fields = ('id', 'query')


class BackendSettingsSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='address_for_check_ssl')

    class Meta:
        model = DashboardSettings
        fields = ('refresh_interval', 'url', 'port', 'protocol')
