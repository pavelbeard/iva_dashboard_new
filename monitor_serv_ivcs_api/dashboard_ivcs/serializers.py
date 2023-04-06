from rest_framework import serializers

from dashboard_ivcs.models import Conference, ConferenceSession, ConferenceSessionActivityStatistic, MediaServer


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ('name',)


class ConferenceSessionActivityStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceSessionActivityStatistic
        fields = ('user_count', 'collect_date')


class ConferenceSessionSerializer(serializers.ModelSerializer):
    parent = ConferenceSerializer()
    activity = ConferenceSessionActivityStatisticSerializer()

    class Meta:
        model = ConferenceSession
        fields = ('state', 'parent', 'activity')


class MediaServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaServer
        fields = '__all__'
