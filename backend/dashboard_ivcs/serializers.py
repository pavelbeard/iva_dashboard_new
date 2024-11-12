from rest_framework import serializers

from dashboard_ivcs.models import Conference, ConferenceSession, ConferenceSessionActivityStatistic, MediaServer, \
    AuditLogRecord, Profile


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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', )


class AuditLogRecordSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = AuditLogRecord
        fields = ('date_created', 'username', 'profile_id',
                  'user_ip', 'severity', 'record_type', 'info_json')

    def get_username(self, obj):
        try:
            profile_id = obj.profile_id
            profile = Profile.objects.using('ivcs').filter(id=profile_id).first()
        except AttributeError:
            profile = None

        if not profile:
            return ""

        profile_serializer = ProfileSerializer(profile)
        return profile_serializer.data['name']
