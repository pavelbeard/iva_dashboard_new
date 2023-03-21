from rest_framework import serializers

from dashboard.models import Target, DashboardSettings


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('id', 'address', 'port')


class BackendSettingsSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='address_for_check_ssl')

    class Meta:
        model = DashboardSettings
        fields = ('url', 'port', 'protocol')