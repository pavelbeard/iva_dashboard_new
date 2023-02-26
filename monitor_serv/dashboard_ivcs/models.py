from django.db import models

# Create your models here.


class AccessLogRecord(models.Model):
    id = models.UUIDField(primary_key=True)
    date = models.DateTimeField()
    execution_time = models.BigIntegerField()
    request_type = models.IntegerField(blank=True, null=True)
    request_path = models.CharField(max_length=2048, blank=True, null=True)
    request_params = models.TextField(blank=True, null=True)
    request_host = models.CharField(max_length=255, blank=True, null=True)
    response_status = models.IntegerField(blank=True, null=True)
    failure_reason = models.CharField(max_length=2048, blank=True, null=True)
    profile_id = models.UUIDField(blank=True, null=True)
    user_ip = models.CharField(max_length=128, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_log_record'


class ActivationRequest(models.Model):
    activation_request_id = models.UUIDField(primary_key=True)
    created = models.DateTimeField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    billing_account = models.OneToOneField('BillingAccount', models.DO_NOTHING)
    domain = models.ForeignKey('Domain', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'activation_request'


class AddressReplacementRule(models.Model):
    search_regex = models.CharField(max_length=255)
    replacement_regex = models.CharField(max_length=255)
    replacement = models.CharField(max_length=255)
    rule_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'address_replacement_rule'


class Answer(models.Model):
    id = models.UUIDField(primary_key=True)
    available_for_all = models.BooleanField()
    last_modified = models.DateTimeField()
    text = models.CharField(max_length=2048, blank=True, null=True)
    owner = models.ForeignKey('Profile', models.DO_NOTHING)
    poll = models.ForeignKey('Poll', models.DO_NOTHING)
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'answer'


class AnswerChoices(models.Model):
    answer = models.OneToOneField(Answer, models.DO_NOTHING, primary_key=True)
    choice = models.ForeignKey('Choice', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'answer_choices'
        unique_together = (('answer', 'choice'),)


class Application(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048, blank=True, null=True)
    domain = models.ForeignKey('Domain', models.DO_NOTHING, blank=True, null=True)
    security_level = models.IntegerField()
    app_id = models.CharField(unique=True, max_length=255)
    app_key = models.CharField(max_length=255)
    privileges = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'application'


class AudioParticipant(models.Model):
    call_id = models.CharField(primary_key=True, max_length=255)
    participant = models.OneToOneField('ConferenceSessionParticipant', models.DO_NOTHING)
    media_state = models.IntegerField()
    media_room = models.ForeignKey('MediaRoom', models.DO_NOTHING)
    subscribe_url = models.CharField(max_length=2048)
    creation_date = models.DateTimeField(blank=True, null=True)
    is_bfcp_on = models.BooleanField()
    data_subscribe_url = models.CharField(max_length=2048, blank=True, null=True)
    protocol = models.IntegerField()
    media_conference = models.ForeignKey('MediaConference', models.DO_NOTHING)
    client_ip = models.CharField(max_length=128, blank=True, null=True)
    fecc_support = models.BooleanField()
    style_override = models.CharField(max_length=512, blank=True, null=True)
    layout_id = models.IntegerField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    client_uri = models.CharField(max_length=128, blank=True, null=True)
    is_incoming = models.BooleanField(blank=True, null=True)
    b2b_call_id = models.CharField(max_length=128, blank=True, null=True)
    b2b_call_server = models.CharField(max_length=128, blank=True, null=True)
    is_moving_media = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_participant'


class AuditLogRecord(models.Model):
    id = models.UUIDField(primary_key=True)
    date_created = models.DateTimeField()
    profile_id = models.UUIDField(blank=True, null=True)
    user_ip = models.CharField(max_length=64, blank=True, null=True)
    severity = models.IntegerField(blank=True, null=True)
    record_type = models.IntegerField(blank=True, null=True)
    info_type = models.IntegerField(blank=True, null=True)
    info_json = models.TextField(blank=True, null=True)
    object_id = models.CharField(max_length=64, blank=True, null=True)
    record_subtype = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_log_record'


class B2BCallHistoryItem(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    params = models.CharField(max_length=128, blank=True, null=True)
    result_uri = models.CharField(max_length=128, blank=True, null=True)
    msg = models.CharField(max_length=128, blank=True, null=True)
    process_time = models.IntegerField(blank=True, null=True)
    b2b_call_server = models.CharField(max_length=128, blank=True, null=True)
    ip = models.CharField(max_length=128, blank=True, null=True)
    from_number = models.CharField(max_length=128, blank=True, null=True)
    to_number = models.CharField(max_length=128, blank=True, null=True)
    is_caller_registered = models.BooleanField(blank=True, null=True)
    is_callee_registered = models.BooleanField(blank=True, null=True)
    signalling_type = models.CharField(max_length=128, blank=True, null=True)
    transport_type = models.CharField(max_length=128, blank=True, null=True)
    is_from_media_service = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'b2b_call_history_item'


class BillingAccount(models.Model):
    billing_account_id = models.UUIDField(primary_key=True)
    activated = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    msisdn = models.CharField(max_length=255)
    pin = models.CharField(max_length=255)
    pin_last_resent = models.DateTimeField()
    user_profile = models.ForeignKey('Profile', models.DO_NOTHING, blank=True, null=True)
    contact_msisdn = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    trial = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'billing_account'


class CallRequest(models.Model):
    id = models.UUIDField(primary_key=True)
    started = models.DateTimeField()
    participant = models.OneToOneField('ConferenceSessionParticipant', models.DO_NOTHING, blank=True, null=True)
    media_room = models.ForeignKey('MediaRoom', models.DO_NOTHING, blank=True, null=True)
    protocol = models.IntegerField()
    dialing = models.BooleanField()
    attempt = models.IntegerField()
    incoming = models.BooleanField()
    media_conference = models.ForeignKey(
        'MediaConference', models.DO_NOTHING, related_name="callrequest_media_conference"
    )
    interconnection_to_media_conference = models.ForeignKey(
        'MediaConference', models.DO_NOTHING, blank=True, null=True,
        related_name="callrequest_interconnection_to_media_conference"
    )
    client_ip = models.CharField(max_length=128, blank=True, null=True)
    client_uri = models.CharField(max_length=128, blank=True, null=True)
    b2b_incoming = models.BooleanField(blank=True, null=True)
    b2b_call_id = models.CharField(max_length=128, blank=True, null=True)
    b2b_call_server = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'call_request'
        unique_together = ("media_conference", "interconnection_to_media_conference")


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True)
    message = models.CharField(max_length=2048, blank=True, null=True)
    send_date = models.DateTimeField()
    author_participant = models.ForeignKey(
        'ConferenceSessionParticipant', models.DO_NOTHING,
        related_name="conferencesessionparticipant_author_participant"
    )
    conference_session = models.ForeignKey('ConferenceSession', models.DO_NOTHING)
    target_participant = models.ForeignKey(
        'ConferenceSessionParticipant', models.DO_NOTHING, blank=True, null=True,
        related_name="conferencesessionparticipant_target_participant"
    )
    deleted = models.BooleanField()
    moderated_by_profile = models.ForeignKey(
        'Profile', models.DO_NOTHING, blank=True, null=True, related_name="profile_moderated_by_profile")
    deleted_by_profile = models.ForeignKey(
        'Profile', models.DO_NOTHING, blank=True, null=True, related_name="profile_deleted_by_profile")
    moderated_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    edited = models.BooleanField()
    attachment_id = models.UUIDField(blank=True, null=True)
    replied_on = models.ForeignKey('self', models.DO_NOTHING, db_column='replied_on', blank=True, null=True)
    moderation_status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'chat_message'
        unique_together = (
            ("moderated_by_profile", "deleted_by_profile"),
            ("author_participant", "target_participant")
        )


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    last_message_at = models.DateTimeField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    chat_avatar_resource = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    is_group = models.BooleanField(blank=True, null=True)
    is_history_access_limited = models.BooleanField()
    call = models.ForeignKey('ChatRoomCall', models.DO_NOTHING, blank=True, null=True)
    last_message_updated_at = models.DateTimeField(blank=True, null=True)
    history_start_from = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chat_room'


class ChatRoomCall(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    state = models.SmallIntegerField()
    created_by = models.UUIDField()
    chat_room = models.ForeignKey(ChatRoom, models.DO_NOTHING)
    media_server_id = models.IntegerField(blank=True, null=True)
    record_path = models.CharField(max_length=4096, blank=True, null=True)
    recording = models.BooleanField(blank=True, null=True)
    presentation_owner_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_room_call'


class ChatRoomCallHistory(models.Model):
    id = models.UUIDField(primary_key=True)
    chat_room = models.ForeignKey(ChatRoom, models.DO_NOTHING)
    created_by = models.UUIDField()
    created_at = models.DateTimeField()
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    media_server_ip = models.CharField(max_length=255, blank=True, null=True)
    document_record = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_room_call_history'


class ChatRoomCallParticipant(models.Model):
    user_id = models.UUIDField(primary_key=True)
    call = models.ForeignKey(ChatRoomCall, models.DO_NOTHING)
    created_at = models.DateTimeField()
    dial_started_at = models.DateTimeField(blank=True, null=True)
    state = models.SmallIntegerField()
    media_state = models.IntegerField()
    protocol = models.IntegerField(blank=True, null=True)
    subscribe_url = models.CharField(max_length=2048, blank=True, null=True)
    publish_url = models.CharField(max_length=2048, blank=True, null=True)
    user_session_id = models.UUIDField(blank=True, null=True)
    channel_close_time = models.DateTimeField(blank=True, null=True)
    media_participant_id = models.UUIDField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    contact_data = models.CharField(max_length=2000, blank=True, null=True)
    join_token = models.CharField(max_length=255, blank=True, null=True)
    data_subscribe_url = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_room_call_participant'
        unique_together = (('user_id', 'call'),)


class ChatRoomCallParticipantHistory(models.Model):
    id = models.UUIDField(primary_key=True)
    call_id = models.UUIDField()
    chat_room = models.ForeignKey(ChatRoom, models.DO_NOTHING)
    user_id = models.UUIDField()
    entered_at = models.DateTimeField()
    left_at = models.DateTimeField(blank=True, null=True)
    user_ip = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    protocol = models.IntegerField(blank=True, null=True)
    leave_reason = models.CharField(max_length=255, blank=True, null=True)
    leave_description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_room_call_participant_history'


class ChatRoomCallParticipantRequest(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(ChatRoomCallParticipant, models.DO_NOTHING)
    call_id = models.UUIDField()
    protocol = models.IntegerField()
    contact_data = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_room_call_participant_request'


class ChatRoomUser(models.Model):
    last_read_at = models.DateTimeField(blank=True, null=True)
    user_id = models.UUIDField()
    chat_room = models.OneToOneField(ChatRoom, models.DO_NOTHING, primary_key=True)
    added_to_chat = models.DateTimeField()
    allow_notifications = models.BooleanField()
    last_delivered_at = models.DateTimeField(blank=True, null=True)
    role = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chat_room_user'
        unique_together = (('chat_room', 'user_id'),)


class Choice(models.Model):
    id = models.UUIDField(primary_key=True)
    choice_order = models.IntegerField()
    choice_value = models.CharField(max_length=2048)
    poll = models.ForeignKey('Poll', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'choice'


class Company(models.Model):
    id = models.UUIDField(primary_key=True)
    blocked = models.BooleanField()
    contract_number = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    domain = models.ForeignKey('Domain', models.DO_NOTHING)
    external_contacts_url = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)
    default_media_group = models.ForeignKey('MediaGroup', models.DO_NOTHING, db_column='default_media_group',
                                            blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class CompanyGroup(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'company_group'


class ConfPlannedReminder(models.Model):
    id = models.UUIDField(primary_key=True)
    reminder_time = models.DateTimeField()
    conference_session = models.ForeignKey('ConferenceSession', models.DO_NOTHING)
    profile = models.ForeignKey('Profile', models.DO_NOTHING, blank=True, null=True)
    reminder_data = models.ForeignKey('ConfReminderData', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conf_planned_reminder'


class ConfReminderData(models.Model):
    id = models.UUIDField(primary_key=True)
    conference = models.ForeignKey('Conference', models.DO_NOTHING, blank=True, null=True)
    interval_minutes = models.SmallIntegerField(blank=True, null=True)
    subject = models.CharField(max_length=256, blank=True, null=True)
    text = models.CharField(max_length=2048, blank=True, null=True)
    reminder_type = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conf_reminder_data'


class Conference(models.Model):
    conference_id = models.UUIDField(primary_key=True)
    duration = models.BigIntegerField()
    invitation_text = models.CharField(max_length=2048, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    audio_translation = models.IntegerField()
    deleted = models.BooleanField()
    description = models.CharField(max_length=2048, blank=True, null=True)
    name = models.CharField(max_length=1024)
    periodical = models.BooleanField()
    schedule = models.CharField(max_length=255, blank=True, null=True)
    attendee_media_state = models.IntegerField()
    attendee_permissions = models.IntegerField()
    conference_type = models.IntegerField()
    run_mode = models.IntegerField()
    update_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey('Profile', models.DO_NOTHING)
    questionnaire = models.ForeignKey('Questionnaire', models.DO_NOTHING, blank=True, null=True)
    subscription_id = models.UUIDField(blank=True, null=True)
    features = models.IntegerField()
    self_registration_enabled = models.BooleanField()
    start_session_number = models.IntegerField()
    conference_number = models.BigIntegerField(unique=True, blank=True, null=True)
    link_sharing_level = models.IntegerField()
    subscribe_limit = models.IntegerField()
    auto_start_stop = models.BooleanField()
    blocked = models.BooleanField(blank=True, null=True)
    conference_level = models.IntegerField(blank=True, null=True)
    media_group = models.ForeignKey('MediaGroup', models.DO_NOTHING, blank=True, null=True)
    media_server = models.ForeignKey('MediaServer', models.DO_NOTHING, blank=True, null=True)
    media_server_distribution = models.SmallIntegerField()
    is_ad_hoc = models.BooleanField()
    ivr_scheme = models.ForeignKey('IvrScheme', models.DO_NOTHING, blank=True, null=True)
    redial_attempts = models.IntegerField()
    redial_interval = models.IntegerField()
    security_level = models.SmallIntegerField()
    previous_conference_number = models.BigIntegerField(blank=True, null=True)
    audio_only_mode = models.BooleanField()
    join_restriction = models.SmallIntegerField()
    layout_id = models.IntegerField(blank=True, null=True)
    style_override = models.CharField(max_length=512, blank=True, null=True)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'conference'


class ConferenceAlert(models.Model):
    id = models.UUIDField(primary_key=True)
    conference_session = models.ForeignKey('ConferenceSession', models.DO_NOTHING)
    message = models.CharField(max_length=2048, blank=True, null=True)
    type = models.IntegerField()
    closable = models.BooleanField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'conference_alert'
        unique_together = (('conference_session', 'type'),)


class ConferenceForDeleteQueue(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'conference_for_delete_queue'


class ConferenceLobbyParticipant(models.Model):
    conference_session_id = models.UUIDField(primary_key=True)
    profile_id = models.UUIDField()
    user_session_id = models.UUIDField(blank=True, null=True)
    event_bus_id = models.CharField(max_length=255, blank=True, null=True)
    ticket_id = models.UUIDField(blank=True, null=True)
    media_participant_id = models.CharField(max_length=60, blank=True, null=True)
    protocol = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'conference_lobby_participant'
        unique_together = (('conference_session_id', 'profile_id'),)


class ConferenceNumber(models.Model):
    id = models.BigIntegerField(primary_key=True)
    release_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference_number'


class ConferenceParticipant(models.Model):
    id = models.UUIDField(primary_key=True)
    allowed_permissions = models.IntegerField()
    color = models.CharField(max_length=255)
    custom_media_state = models.IntegerField(blank=True, null=True)
    deleted = models.BooleanField()
    denied_permissions = models.IntegerField()
    invite_response_type = models.IntegerField()
    unsubscribed = models.BooleanField()
    profile = models.ForeignKey('Profile', models.DO_NOTHING)
    conference = models.ForeignKey(Conference, models.DO_NOTHING)
    dial_at_start = models.BooleanField(blank=True, null=True)
    self_registered = models.BooleanField()
    invite_response_date = models.DateTimeField(blank=True, null=True)
    inform_by_sms = models.BooleanField(blank=True, null=True)
    cascade_type = models.IntegerField(blank=True, null=True)
    max_bitrate = models.BigIntegerField(blank=True, null=True)
    layout_id = models.IntegerField(blank=True, null=True)
    show_own_video = models.BooleanField(blank=True, null=True)
    output_audio_gain = models.IntegerField(blank=True, null=True)
    main_stream_video_codec = models.SmallIntegerField(blank=True, null=True)
    main_stream_audio_codec = models.SmallIntegerField(blank=True, null=True)
    additional_stream_video_codec = models.SmallIntegerField(blank=True, null=True)
    video_preset = models.SmallIntegerField(blank=True, null=True)
    encryption_type = models.SmallIntegerField(blank=True, null=True)
    encryption_mandatory = models.BooleanField(blank=True, null=True)
    fec_scheme = models.SmallIntegerField(blank=True, null=True)
    adaptive_bitrate = models.BooleanField(blank=True, null=True)
    keep_in_conference = models.BooleanField(blank=True, null=True)
    main_codec_width = models.SmallIntegerField(blank=True, null=True)
    main_codec_height = models.SmallIntegerField(blank=True, null=True)
    main_codec_fps = models.SmallIntegerField(blank=True, null=True)
    additional_codec_width = models.SmallIntegerField(blank=True, null=True)
    additional_codec_height = models.SmallIntegerField(blank=True, null=True)
    additional_codec_fps = models.SmallIntegerField(blank=True, null=True)
    show_own_name = models.BooleanField(blank=True, null=True)
    bfcp_mode = models.SmallIntegerField(blank=True, null=True)
    input_audio_gain = models.IntegerField(blank=True, null=True)
    style_override = models.CharField(max_length=512, blank=True, null=True)
    add_content_screen_mode = models.SmallIntegerField(blank=True, null=True)
    sip_transport_protocol = models.SmallIntegerField(blank=True, null=True)
    role = models.SmallIntegerField()
    interpreter_lang_pair = models.SmallIntegerField()
    broadcast_language = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference_participant'
        unique_together = (('conference', 'profile'),)


class ConferenceQuality(models.Model):
    id = models.IntegerField(primary_key=True)
    audio_quality = models.IntegerField()
    max_speaker_count = models.IntegerField()
    fps = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    protocol = models.IntegerField()
    video_quality = models.IntegerField()
    min_video_quality = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'conference_quality'


class ConferenceSession(models.Model):
    id = models.UUIDField(primary_key=True)
    duration = models.BigIntegerField()
    invitation_text = models.CharField(max_length=2048, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    actual_start_date = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField()
    description = models.CharField(max_length=2048, blank=True, null=True)
    name = models.CharField(max_length=1024)
    session_number = models.IntegerField(blank=True, null=True)
    attendee_media_state = models.IntegerField()
    attendee_permissions = models.IntegerField()
    conference_type = models.IntegerField()
    run_mode = models.IntegerField()
    state = models.CharField(max_length=255, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    parent = models.ForeignKey(Conference, models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('Profile', models.DO_NOTHING)
    whiteboard = models.ForeignKey('Whiteboard', models.DO_NOTHING, blank=True, null=True)
    frame_id = models.UUIDField(unique=True)
    audio_translation = models.IntegerField()
    features = models.IntegerField()
    self_registration_enabled = models.BooleanField()
    self_registration_active = models.BooleanField()
    link_sharing_level = models.IntegerField()
    subscribe_limit = models.IntegerField()
    auto_start_stop = models.BooleanField()
    media_server_distribution = models.SmallIntegerField()
    fixed_layout_configuration = models.ForeignKey('FixedLayoutConfiguration', models.DO_NOTHING, blank=True, null=True)
    ivr_scheme = models.ForeignKey('IvrScheme', models.DO_NOTHING, blank=True, null=True)
    redial_attempts = models.IntegerField()
    redial_interval = models.IntegerField()
    audio_only_mode = models.BooleanField()
    join_restriction = models.SmallIntegerField()
    alert_message = models.CharField(max_length=2048, blank=True, null=True)
    alert_duration = models.BigIntegerField(blank=True, null=True)
    starred = models.BooleanField(blank=True, null=True)
    style_override = models.CharField(max_length=512, blank=True, null=True)
    layout_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField()
    last_media_session_start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference_session'


class ConferenceSessionActivityStatistic(models.Model):
    collect_date = models.DateTimeField()
    frame_count = models.IntegerField(blank=True, null=True)
    speaker_count = models.IntegerField(blank=True, null=True)
    user_count = models.IntegerField(blank=True, null=True)
    conference_session = models.OneToOneField(ConferenceSession, models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=1024)
    domain_id = models.UUIDField()
    owner_id = models.UUIDField()
    conference_type = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'conference_session_activity_statistic'
        unique_together = (('conference_session', 'collect_date'),)


class ConferenceSessionParticipant(models.Model):
    id = models.UUIDField(primary_key=True)
    allowed_permissions = models.IntegerField()
    color = models.CharField(max_length=255)
    custom_media_state = models.IntegerField(blank=True, null=True)
    deleted = models.BooleanField()
    denied_permissions = models.IntegerField()
    invite_response_type = models.IntegerField()
    unsubscribed = models.BooleanField()
    entered_by_ticket = models.UUIDField(blank=True, null=True)
    was_on_conference = models.BooleanField()
    profile = models.ForeignKey('Profile', models.DO_NOTHING)
    conference_session = models.ForeignKey(ConferenceSession, models.DO_NOTHING)
    dial_at_start = models.BooleanField(blank=True, null=True)
    self_registered = models.BooleanField()
    invite_response_date = models.DateTimeField(blank=True, null=True)
    inform_by_sms = models.BooleanField(blank=True, null=True)
    cascade_type = models.IntegerField(blank=True, null=True)
    max_bitrate = models.BigIntegerField(blank=True, null=True)
    layout_id = models.IntegerField(blank=True, null=True)
    show_own_video = models.BooleanField(blank=True, null=True)
    output_audio_gain = models.IntegerField(blank=True, null=True)
    fixed_layout_configuration = models.ForeignKey('FixedLayoutConfiguration', models.DO_NOTHING, blank=True, null=True)
    main_stream_video_codec = models.SmallIntegerField(blank=True, null=True)
    main_stream_audio_codec = models.SmallIntegerField(blank=True, null=True)
    additional_stream_video_codec = models.SmallIntegerField(blank=True, null=True)
    video_preset = models.SmallIntegerField(blank=True, null=True)
    encryption_type = models.SmallIntegerField(blank=True, null=True)
    encryption_mandatory = models.BooleanField(blank=True, null=True)
    periods_notification = models.BooleanField()
    fec_scheme = models.SmallIntegerField(blank=True, null=True)
    adaptive_bitrate = models.BooleanField(blank=True, null=True)
    keep_in_conference = models.BooleanField(blank=True, null=True)
    main_codec_width = models.SmallIntegerField(blank=True, null=True)
    main_codec_height = models.SmallIntegerField(blank=True, null=True)
    main_codec_fps = models.SmallIntegerField(blank=True, null=True)
    additional_codec_width = models.SmallIntegerField(blank=True, null=True)
    additional_codec_height = models.SmallIntegerField(blank=True, null=True)
    additional_codec_fps = models.SmallIntegerField(blank=True, null=True)
    show_own_name = models.BooleanField(blank=True, null=True)
    bfcp_mode = models.SmallIntegerField(blank=True, null=True)
    input_audio_gain = models.IntegerField(blank=True, null=True)
    style_override = models.CharField(max_length=512, blank=True, null=True)
    add_content_screen_mode = models.SmallIntegerField(blank=True, null=True)
    sip_transport_protocol = models.SmallIntegerField(blank=True, null=True)
    role = models.SmallIntegerField()
    interpreter_lang_pair = models.SmallIntegerField()
    broadcast_language = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference_session_participant'
        unique_together = (('conference_session', 'profile'),)


class ConferenceSessionParticipantStatistics(models.Model):
    conference_session_participant = models.OneToOneField(ConferenceSessionParticipant, models.DO_NOTHING,
                                                          primary_key=True)
    profile_id = models.UUIDField()
    conference_session_id = models.UUIDField()
    user_agents = models.IntegerField()
    first_join_date = models.DateTimeField(blank=True, null=True)
    last_leave_date = models.DateTimeField(blank=True, null=True)
    invite_response_type = models.SmallIntegerField()
    invitation_status = models.SmallIntegerField()
    engagement = models.DecimalField(max_digits=65535, decimal_places=65535)
    role = models.SmallIntegerField()
    was_on_conference = models.BooleanField()
    deleted = models.BooleanField()
    past_all_polls = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'conference_session_participant_statistics'


class ConferenceSessionPeriodStatistic(models.Model):
    active_speaker = models.BooleanField()
    end_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField()
    conference_session = models.OneToOneField(ConferenceSession, models.DO_NOTHING, primary_key=True)
    max_users = models.IntegerField(blank=True, null=True)
    max_speakers = models.IntegerField(blank=True, null=True)
    max_frame = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference_session_period_statistic'
        unique_together = (('conference_session', 'active_speaker', 'start_date'),)


class ConferenceSessionStatisticTimer(models.Model):
    collect_date = models.DateTimeField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'conference_session_statistic_timer'


class ConferenceSessionStatistics(models.Model):
    conference_session = models.OneToOneField(ConferenceSession, models.DO_NOTHING, primary_key=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    owner_id = models.UUIDField(blank=True, null=True)
    domain_id = models.UUIDField(blank=True, null=True)
    conference_type = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=1024, blank=True, null=True)
    invited_participants_count = models.BigIntegerField()
    invited_and_visited_participants_count = models.BigIntegerField()
    registered_participants_count = models.BigIntegerField()
    registered_and_visited_participants_count = models.BigIntegerField()
    guests_count = models.BigIntegerField()
    visited_participants_count = models.BigIntegerField()
    past_all_polls_participants_count = models.BigIntegerField()
    engagement = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    web_clients_count = models.IntegerField(blank=True, null=True)
    desktop_clients_count = models.IntegerField(blank=True, null=True)
    ios_clients_count = models.IntegerField(blank=True, null=True)
    android_clients_count = models.IntegerField(blank=True, null=True)
    room_clients_count = models.IntegerField(blank=True, null=True)
    sip_clients_count = models.IntegerField(blank=True, null=True)
    h323_clients_count = models.IntegerField(blank=True, null=True)
    s4b_clients_count = models.IntegerField(blank=True, null=True)
    rtsp_clients_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference_session_statistics'


class ConferenceTemplate(models.Model):
    id = models.UUIDField(primary_key=True)
    audio_translation = models.IntegerField()
    deleted = models.BooleanField()
    description = models.CharField(max_length=1024, blank=True, null=True)
    icon_type = models.IntegerField()
    name = models.CharField(max_length=1024)
    owner_type = models.IntegerField()
    attendee_media_state = models.IntegerField()
    attendee_permissions = models.IntegerField()
    conference_type = models.IntegerField()
    run_mode = models.IntegerField()
    owner = models.ForeignKey('Profile', models.DO_NOTHING, blank=True, null=True)
    domain = models.ForeignKey('Domain', models.DO_NOTHING)
    features = models.IntegerField()
    self_registration_enabled = models.BooleanField()
    link_sharing_level = models.IntegerField()
    subscribe_limit = models.IntegerField()
    auto_start_stop = models.BooleanField()
    layout_preference = models.IntegerField()
    media_server_distribution = models.SmallIntegerField()
    ivr_scheme = models.ForeignKey('IvrScheme', models.DO_NOTHING, blank=True, null=True)
    redial_attempts = models.IntegerField()
    redial_interval = models.IntegerField()
    audio_only_mode = models.BooleanField()
    join_restriction = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'conference_template'


class ConferenceTranscript(models.Model):
    conference_session_participant_id = models.UUIDField()
    conference_session_id = models.UUIDField()
    phrase = models.CharField(max_length=8192)
    phrase_timestamp = models.BigIntegerField()
    duration_ms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference_transcript'


class ConnectionHolder(models.Model):
    connection_holder = models.CharField(max_length=100, blank=True, null=True)
    node_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'connection_holder'


class Contact(models.Model):
    contact_type = models.CharField(max_length=3)
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    note = models.CharField(max_length=500, blank=True, null=True)
    owner_user = models.ForeignKey('Profile', models.DO_NOTHING, related_name="profile_owner_user")
    user_profile = models.ForeignKey(
        'Profile', models.DO_NOTHING, blank=True, null=True, related_name="profile_user_profile")
    primary_email = models.CharField(max_length=255, blank=True, null=True)
    primary_phone = models.CharField(max_length=512, blank=True, null=True)
    tag_list = models.CharField(max_length=1024, blank=True, null=True)
    authorized = models.BooleanField(blank=True, null=True)
    linked_profile = models.ForeignKey('Profile', models.DO_NOTHING, blank=True, null=True)
    personal = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'
        unique_together = (('owner_user', 'user_profile'),)


class ConvertedPage(models.Model):
    id = models.UUIDField(primary_key=True)
    order_col = models.IntegerField()
    document_resource = models.ForeignKey('FsNode', models.DO_NOTHING, db_column='document_resource')
    image_resource = models.ForeignKey('Resources', models.DO_NOTHING, db_column='image_resource')

    class Meta:
        managed = False
        db_table = 'converted_page'


class CsiAnswer(models.Model):
    answer_type = models.CharField(max_length=31)
    id = models.UUIDField(primary_key=True)
    answer_date = models.DateTimeField()
    ip_address = models.CharField(max_length=255)
    discrete_value = models.IntegerField(blank=True, null=True)
    conference_session = models.ForeignKey(ConferenceSession, models.DO_NOTHING)
    profile = models.ForeignKey('Profile', models.DO_NOTHING)
    question = models.ForeignKey('CsiQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'csi_answer'


class CsiQuestion(models.Model):
    question_type = models.CharField(max_length=31)
    id = models.UUIDField(primary_key=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField()
    start_date = models.DateTimeField()
    text = models.CharField(max_length=2048)
    max_value = models.IntegerField(blank=True, null=True)
    min_value = models.IntegerField(blank=True, null=True)
    domain = models.ForeignKey('Domain', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'csi_question'


class DelayedMediaAction(models.Model):
    id = models.UUIDField(primary_key=True)
    conference_id = models.CharField(max_length=64)
    action_type = models.CharField(max_length=64)
    media_server = models.ForeignKey('MediaServer', models.DO_NOTHING, blank=True, null=True)
    info_json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delayed_media_action'


class DelayedSms(models.Model):
    id = models.UUIDField(primary_key=True)
    creation_date = models.DateTimeField()
    from_phone = models.CharField(max_length=16, blank=True, null=True)
    message = models.CharField(max_length=2048)
    payer = models.CharField(max_length=16, blank=True, null=True)
    to_phone = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'delayed_sms'


class Device(models.Model):
    id = models.UUIDField(primary_key=True)
    mac_address = models.CharField(unique=True, max_length=255)
    profile = models.ForeignKey('Profile', models.DO_NOTHING)
    device_model = models.ForeignKey('DeviceModel', models.DO_NOTHING)
    config_overridden = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DeviceModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    vendor = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='vendor')
    configs_path = models.CharField(max_length=255)
    personal_config = models.UUIDField()
    personal_config_name = models.CharField(max_length=255)
    general_config = models.UUIDField(blank=True, null=True)
    general_config_name = models.CharField(max_length=255, blank=True, null=True)
    protocols = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_model'


class DeviceModelFirmwareFiles(models.Model):
    device_model = models.OneToOneField(DeviceModel, models.DO_NOTHING, primary_key=True)
    firmwarefiles_resource_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'device_model_firmware_files'
        unique_together = (('device_model', 'firmwarefiles_resource_id'),)


class DocumentAlias(models.Model):
    alias = models.CharField(primary_key=True, max_length=20)
    locale = models.CharField(max_length=5)
    absolute_link = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'document_alias'
        unique_together = (('alias', 'locale'),)


class Domain(models.Model):
    default_sender_email = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    support_email = models.CharField(max_length=255, blank=True, null=True)
    domain_id = models.UUIDField(primary_key=True)
    logo_resource_id = models.UUIDField(blank=True, null=True)
    external_login_url = models.CharField(max_length=255, blank=True, null=True)
    ga_account = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255)
    password_modification = models.BooleanField()
    private_office_url = models.CharField(max_length=255, blank=True, null=True)
    registration = models.BooleanField()
    bw_checker_link = models.CharField(max_length=255, blank=True, null=True)
    send_missed_notification = models.BooleanField()
    send_sms = models.BooleanField()
    frame = models.BooleanField()
    outgoing_call = models.BooleanField()
    send_sms_from_owner = models.BooleanField()
    calendar_organizer_email = models.CharField(max_length=255, blank=True, null=True)
    support_phone = models.CharField(max_length=255, blank=True, null=True)
    big_logo_resource_id = models.UUIDField(blank=True, null=True)
    send_https_links = models.BooleanField()
    features = models.IntegerField()
    promo_site_url = models.CharField(max_length=255, blank=True, null=True)
    send_thirdparty_notification = models.BooleanField()
    min_phone_length = models.IntegerField()
    max_phone_length = models.IntegerField()
    conference_reference_host = models.CharField(max_length=255, blank=True, null=True)
    sms_tariff_url = models.CharField(max_length=255, blank=True, null=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    auto_record = models.BooleanField()
    record_deletion_enabled = models.BooleanField()
    external_contacts_url = models.CharField(max_length=255, blank=True, null=True)
    record_live_interval_in_days = models.IntegerField()
    avaible_connection_configuration = models.BooleanField()
    notify_about_sms = models.BooleanField(blank=True, null=True)
    email_to_send_sms = models.CharField(max_length=255, blank=True, null=True)
    fixed_locale = models.CharField(max_length=255, blank=True, null=True)
    leave_conference_redirect = models.CharField(max_length=255, blank=True, null=True)
    support_url = models.CharField(max_length=255, blank=True, null=True)
    registration_url = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.BooleanField()
    event_logo_resource_id = models.UUIDField(blank=True, null=True)
    frame_logo_resource_id = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domain'


class DtmfCommand(models.Model):
    command = models.CharField(primary_key=True, max_length=255)
    code = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dtmf_command'


class EmailInvitation(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=255)
    source_user = models.ForeignKey('Profile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'email_invitation'
        unique_together = (('source_user', 'email'),)


class EventChannels(models.Model):
    event_channel_id = models.UUIDField(primary_key=True)
    owner_node = models.CharField(max_length=255)
    user_session = models.ForeignKey('UserSessions', models.DO_NOTHING)
    bus_id = models.CharField(max_length=255, blank=True, null=True)
    origin = models.CharField(max_length=2048, blank=True, null=True)
    active_call_id = models.UUIDField(blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_channels'


class ExternalCall(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField()
    expires = models.DateTimeField()
    url = models.CharField(max_length=4096)
    media_room = models.ForeignKey('MediaRoom', models.DO_NOTHING)
    media_conference = models.ForeignKey('MediaConference', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'external_call'


class FixedLayoutConfiguration(models.Model):
    id = models.UUIDField(primary_key=True)
    layout = models.ForeignKey('Layout', models.DO_NOTHING)
    conference_session = models.ForeignKey(ConferenceSession, models.DO_NOTHING)
    created_at = models.DateTimeField()
    periodicity = models.SmallIntegerField(blank=True, null=True)
    cell_mapping = models.CharField(max_length=32768, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fixed_layout_configuration'


class FsNode(models.Model):
    node_type = models.IntegerField()
    id = models.UUIDField(primary_key=True)
    conference_session_id = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()
    name = models.CharField(max_length=1024)
    version_num = models.IntegerField()
    permission_type = models.IntegerField(blank=True, null=True)
    convertation_percent = models.IntegerField(blank=True, null=True)
    format = models.IntegerField(blank=True, null=True)
    available_for_download = models.BooleanField(blank=True, null=True)
    associated_user = models.UUIDField()
    parent = models.ForeignKey(
        'self', models.DO_NOTHING, db_column='parent', blank=True, null=True, related_name="self_parent")
    linked_node = models.ForeignKey(
        'self', models.DO_NOTHING, db_column='linked_node', blank=True, null=True, related_name="self_linked_node")
    resource = models.ForeignKey('Resources', models.DO_NOTHING, db_column='resource', blank=True, null=True)
    conversion_fail_reason = models.IntegerField(blank=True, null=True)
    storage_results_uri = models.CharField(max_length=255, blank=True, null=True)
    storage_uri = models.CharField(max_length=255, blank=True, null=True)
    conversion_state = models.IntegerField(blank=True, null=True)
    min_storage_date = models.DateTimeField(blank=True, null=True)
    associated_object_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fs_node'
        unique_together = ("parent", "linked_node")


class GkNeighbor(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    send_prefixes = models.CharField(max_length=256, blank=True, null=True)
    recv_prefixes = models.CharField(max_length=256, blank=True, null=True)
    timeout = models.IntegerField(blank=True, null=True)
    max_send_tries = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gk_neighbor'


class GroupUsers(models.Model):
    profile = models.OneToOneField('Profile', models.DO_NOTHING, primary_key=True)
    group = models.ForeignKey('UserGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'group_users'
        unique_together = (('profile', 'group'),)


class GroupsProfiles(models.Model):
    group = models.OneToOneField(CompanyGroup, models.DO_NOTHING, primary_key=True)
    profile = models.ForeignKey('Profile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'groups_profiles'
        unique_together = (('group', 'profile'),)


class IceServer(models.Model):
    url = models.CharField(max_length=4096)
    user_name = models.CharField(max_length=128, blank=True, null=True)
    credential = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ice_server'


class Inquiry(models.Model):
    id = models.UUIDField(primary_key=True)
    last_modified = models.DateTimeField()
    state = models.CharField(max_length=255)
    conference_session = models.ForeignKey(ConferenceSession, models.DO_NOTHING)
    owner = models.ForeignKey('Profile', models.DO_NOTHING)
    poll = models.ForeignKey('Poll', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inquiry'


class InstalledUpdates(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    major_version = models.IntegerField()
    minor_version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'installed_updates'
        unique_together = (('name', 'major_version', 'minor_version'),)


class InterconnectionParticipant(models.Model):
    id = models.UUIDField(primary_key=True)
    is_bfcp_on = models.BooleanField()
    is_incoming = models.BooleanField()
    protocol = models.IntegerField()
    data_subscribe_url = models.CharField(max_length=2048)
    subscribe_url = models.CharField(max_length=2048)
    connected_media_conference = models.ForeignKey(
        'MediaConference', models.DO_NOTHING, blank=True, null=True,
        related_name="mediaconference_connected_media_conference"
    )
    media_conference = models.ForeignKey(
        'MediaConference', models.DO_NOTHING,
        related_name="mediaconference_media_conference"
    )
    media_room = models.ForeignKey('MediaRoom', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'interconnection_participant'
        unique_together = ("connected_media_conference", "media_conference")


class InterconnectionSettings(models.Model):
    id = models.UUIDField(primary_key=True)
    media_group_from = models.ForeignKey(
        'MediaGroup', models.DO_NOTHING, related_name="mediagroup_media_group_from")
    media_group_to = models.ForeignKey(
        'MediaGroup', models.DO_NOTHING)
    conference_session = models.ForeignKey(
        ConferenceSession, models.DO_NOTHING, blank=True, null=True,
        related_name="mediagroup_conference_session"
    )
    from_layout_id = models.IntegerField()
    to_layout_id = models.IntegerField()
    max_bitrate = models.IntegerField()
    from_layout_style_override = models.CharField(max_length=512, blank=True, null=True)
    to_layout_style_override = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interconnection_settings'
        unique_together = (
            ('media_group_from', 'media_group_to', 'conference_session'),
            ('media_group_from', 'media_group_to'),
        )


class Ivr(models.Model):
    type = models.SmallIntegerField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    text_output_x = models.IntegerField(blank=True, null=True)
    text_output_y = models.IntegerField(blank=True, null=True)
    text_font_size = models.IntegerField(blank=True, null=True)
    text_color = models.IntegerField(blank=True, null=True)
    scheme = models.ForeignKey('IvrScheme', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ivr'
        unique_together = (('type', 'scheme'),)


class IvrCallHistoryItem(models.Model):
    id = models.UUIDField(primary_key=True)
    from_number = models.CharField(max_length=255)
    to_number = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    redirect_to_event = models.UUIDField(blank=True, null=True)
    termination_status = models.IntegerField()
    termination_reason = models.CharField(max_length=255, blank=True, null=True)
    steps_history = models.TextField(blank=True, null=True)
    client_ip = models.CharField(max_length=32, blank=True, null=True)
    redirect_to_profile = models.UUIDField(blank=True, null=True)
    b2b_call_id = models.CharField(max_length=128, blank=True, null=True)
    b2b_call_server = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivr_call_history_item'


class IvrScheme(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048, blank=True, null=True)
    scheme_number = models.BigIntegerField(unique=True)
    is_default = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'ivr_scheme'


class Layout(models.Model):
    name = models.CharField(max_length=255)
    type = models.IntegerField(blank=True, null=True)
    cell_count = models.IntegerField()
    cell_config = models.CharField(max_length=32768, blank=True, null=True)
    fixed_layout_type = models.CharField(max_length=32, blank=True, null=True)
    is_system = models.BooleanField()
    is_deleted = models.BooleanField()
    description = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layout'


class Ldap(models.Model):
    id = models.UUIDField(primary_key=True)
    domain = models.ForeignKey(Domain, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    domain_alias = models.CharField(max_length=32)
    order_number = models.IntegerField()
    server_url = models.CharField(max_length=255)
    bind_dn = models.CharField(max_length=255)
    bind_password = models.CharField(max_length=255)
    base_dn = models.CharField(max_length=255)
    base_filter = models.CharField(max_length=255)
    authentication = models.BooleanField()
    address_book = models.BooleanField()
    event_creation = models.BooleanField()
    auto_synchronization = models.BooleanField()
    create_on_ldap_invite = models.BooleanField()
    user_id = models.CharField(max_length=255)
    user_login = models.CharField(max_length=255)
    user_display_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_middle_name = models.CharField(max_length=255)
    user_second_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    user_phone_number = models.CharField(max_length=255)
    user_description = models.CharField(max_length=255)
    deleted = models.BooleanField()
    user_avatar = models.CharField(max_length=255, blank=True, null=True)
    alternative_server_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ldap'
        unique_together = (('domain', 'domain_alias'),)


class Locale(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    language = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'locale'
        unique_together = (('key', 'language'),)


class LocaleResource(models.Model):
    key = models.TextField(primary_key=True)
    language = models.TextField()
    resource_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'locale_resource'
        unique_together = (('key', 'language'),)


class LoginToken(models.Model):
    login_token_id = models.UUIDField(primary_key=True)
    date = models.DateTimeField()
    profile = models.ForeignKey('Profile', models.DO_NOTHING)
    token_type = models.CharField(max_length=15)
    user_agent = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=15)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'login_token'


class LogsExportsHistory(models.Model):
    id = models.UUIDField(primary_key=True)
    min_date_from = models.DateTimeField(blank=True, null=True)
    max_date_to = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs_exports_history'


class MediaConference(models.Model):
    id = models.UUIDField(primary_key=True)
    is_main = models.BooleanField()
    media_group = models.ForeignKey('MediaGroup', models.DO_NOTHING)
    media_room = models.ForeignKey('MediaRoom', models.DO_NOTHING)
    media_server = models.ForeignKey('MediaServer', models.DO_NOTHING)
    is_deleted = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_conference'
        unique_together = (('media_room', 'is_main'),)


class MediaGroup(models.Model):
    name = models.CharField(unique=True, max_length=128)
    is_default = models.BooleanField()
    subnet_masks = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_group'


class MediaGroupMediaServer(models.Model):
    media_group = models.ForeignKey(MediaGroup, models.DO_NOTHING, blank=True, null=True)
    media_server = models.ForeignKey('MediaServer', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_group_media_server'
        unique_together = (('media_group', 'media_server'),)


class MediaParticipant(models.Model):
    id = models.UUIDField(primary_key=True)
    hand_state = models.BooleanField()
    webinar_guest = models.BooleanField()
    media_room = models.ForeignKey('MediaRoom', models.DO_NOTHING)
    conference_session_participant = models.OneToOneField(ConferenceSessionParticipant, models.DO_NOTHING, blank=True,
                                                          null=True)
    user_session_id = models.UUIDField(unique=True)
    creation_date = models.DateTimeField()
    screenshare_state = models.IntegerField(blank=True, null=True)
    screenshare_stream_id = models.UUIDField(blank=True, null=True)
    speaker_state = models.IntegerField(blank=True, null=True)
    speaker_stream_id = models.UUIDField(blank=True, null=True)
    screenshare_publish_url = models.CharField(max_length=2048, blank=True, null=True)
    screenshare_subscribe_url = models.CharField(max_length=2048, blank=True, null=True)
    speaker_publish_url = models.CharField(max_length=2048, blank=True, null=True)
    speaker_subscribe_url = models.CharField(max_length=2048, blank=True, null=True)
    protocol = models.IntegerField()
    max_media_profile = models.IntegerField(blank=True, null=True)
    desired_media_profile = models.IntegerField(blank=True, null=True)
    channel_close_time = models.DateTimeField(blank=True, null=True)
    media_conference = models.ForeignKey(MediaConference, models.DO_NOTHING)
    camera = models.CharField(max_length=512, blank=True, null=True)
    microphone = models.CharField(max_length=512, blank=True, null=True)
    speakers = models.CharField(max_length=512, blank=True, null=True)
    style_override = models.CharField(max_length=512, blank=True, null=True)
    layout_id = models.IntegerField(blank=True, null=True)
    layout_preset = models.SmallIntegerField(blank=True, null=True)
    translation_direction = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_participant'


class MediaParticipantHistory(models.Model):
    id = models.UUIDField(primary_key=True)
    enter_date = models.DateTimeField()
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    leave_date = models.DateTimeField(blank=True, null=True)
    media_participant_id = models.CharField(max_length=40, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    ticket_link = models.CharField(max_length=2048, blank=True, null=True)
    ticket_comment = models.CharField(max_length=2048, blank=True, null=True)
    is_system = models.BooleanField()
    conference_session = models.ForeignKey(ConferenceSession, models.DO_NOTHING)
    conference_session_participant = models.ForeignKey(ConferenceSessionParticipant, models.DO_NOTHING, blank=True,
                                                       null=True)
    leave_reason = models.CharField(max_length=255, blank=True, null=True)
    vvoip_terminate_reason = models.CharField(max_length=255, blank=True, null=True)
    resolved = models.BooleanField(blank=True, null=True)
    media_conference_id = models.CharField(max_length=36, blank=True, null=True)
    media_server_ip = models.CharField(max_length=16, blank=True, null=True)
    protocol = models.CharField(max_length=16, blank=True, null=True)
    is_incoming = models.BooleanField(blank=True, null=True)
    client_uri = models.CharField(max_length=128, blank=True, null=True)
    vvoip_terminate_description = models.CharField(max_length=128, blank=True, null=True)
    media_server_participant_id = models.CharField(max_length=40, blank=True, null=True)
    media_server_sec_participant_id = models.CharField(max_length=40, blank=True, null=True)
    b2b_call_id = models.CharField(max_length=128, blank=True, null=True)
    b2b_call_server = models.CharField(max_length=128, blank=True, null=True)
    user_session_id = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_participant_history'


class MediaProfile(models.Model):
    subscription_type = models.CharField(max_length=31)
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=4096, blank=True, null=True)
    name = models.CharField(max_length=1024)
    protocol = models.IntegerField()
    publish_fps = models.IntegerField()
    publish_height = models.IntegerField()
    publish_width = models.IntegerField()
    mosaic_crf = models.IntegerField(blank=True, null=True)
    mosaic_fps = models.IntegerField(blank=True, null=True)
    mosaic_height = models.IntegerField(blank=True, null=True)
    mosaic_width = models.IntegerField(blank=True, null=True)
    mosaic_bitrate = models.IntegerField(blank=True, null=True)
    video_quality = models.IntegerField()
    min_video_quality = models.IntegerField()
    audio_quality = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'media_profile'


class MediaPublication(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField()
    expires = models.DateTimeField(blank=True, null=True)
    fps = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    url = models.CharField(max_length=4096)
    media_room = models.ForeignKey('MediaRoom', models.DO_NOTHING)
    layout = models.ForeignKey(Layout, models.DO_NOTHING)
    media_conference = models.ForeignKey(MediaConference, models.DO_NOTHING, blank=True, null=True)
    type = models.SmallIntegerField()
    style_override = models.CharField(max_length=512, blank=True, null=True)
    connection_state = models.SmallIntegerField(blank=True, null=True)
    last_connection_error = models.CharField(max_length=128, blank=True, null=True)
    connection_state_change_date = models.DateTimeField(blank=True, null=True)
    internal_server = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_publication'


class MediaRoom(models.Model):
    id = models.UUIDField(primary_key=True)
    room_state = models.IntegerField()
    speaker_preset = models.IntegerField()
    conference_session = models.OneToOneField(ConferenceSession, models.DO_NOTHING)
    recording = models.BooleanField()
    reoording_expiration_date = models.DateTimeField(blank=True, null=True)
    recording_start_date = models.DateTimeField(blank=True, null=True)
    current_record_file_path = models.CharField(max_length=4096, blank=True, null=True)
    subscribe_limit = models.IntegerField()
    current_data_record_file_path = models.TextField(blank=True, null=True)
    transcribing_start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_room'


class MediaServer(models.Model):
    address = models.CharField(max_length=255)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'media_server'


class Message(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    message = models.TextField()
    chat_room = models.ForeignKey(ChatRoom, models.DO_NOTHING)
    system_type = models.SmallIntegerField()
    created_by = models.UUIDField()
    attachment_id = models.UUIDField(blank=True, null=True)
    deleted = models.BooleanField()
    replied_on = models.ForeignKey(
        'self', models.DO_NOTHING, db_column='replied_on',
        blank=True, null=True, related_name="self_replied_on"
    )
    edited = models.BooleanField(blank=True, null=True)
    forward_message_created_at = models.DateTimeField(blank=True, null=True)
    forward_message_created_by = models.UUIDField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'message'
        unique_together = (('chat_room', 'created_at'), ("replied_on",))


class MonitorIcmp(models.Model):
    id = models.UUIDField(primary_key=True)
    host = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, blank=True, null=True)
    status = models.BooleanField()
    check_date = models.DateTimeField(blank=True, null=True)
    last_success_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitor_icmp'


class MonitorMcu(models.Model):
    id = models.UUIDField(primary_key=True)
    host = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, blank=True, null=True)
    status = models.BooleanField()
    check_date = models.DateTimeField(blank=True, null=True)
    last_success_date = models.DateTimeField(blank=True, null=True)
    login = models.CharField(max_length=256)
    domain = models.CharField(max_length=256)
    password = models.CharField(max_length=100, blank=True, null=True)
    conference_count = models.IntegerField(blank=True, null=True)
    user_count = models.IntegerField(blank=True, null=True)
    cpu_load = models.IntegerField(blank=True, null=True)
    error = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitor_mcu'


class Notification(models.Model):
    notification_type = models.CharField(max_length=15)
    id = models.UUIDField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    is_date_changed = models.BooleanField(blank=True, null=True)
    approved = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey('Profile', models.DO_NOTHING, related_name="profile_user")
    conference = models.ForeignKey(Conference, models.DO_NOTHING, blank=True, null=True)
    source_user = models.ForeignKey('Profile', models.DO_NOTHING, blank=True, null=True,
                                    related_name="profile_source_user")
    conference_session = models.ForeignKey(ConferenceSession, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification'
        unique_together = ("user", "source_user")


class Poll(models.Model):
    id = models.UUIDField(primary_key=True)
    allows_reanswer = models.IntegerField()
    anonymous = models.IntegerField()
    answer_type = models.CharField(max_length=255)
    poll_order = models.IntegerField()
    required = models.IntegerField()
    show_results_after_answer = models.IntegerField()
    show_results_only_author = models.IntegerField()
    text = models.CharField(max_length=2048)

    class Meta:
        managed = False
        db_table = 'poll'


class Presentation(models.Model):
    presentation_type = models.IntegerField()
    id = models.UUIDField(primary_key=True)
    cursorleft = models.IntegerField()
    cursortop = models.IntegerField()
    cursorvisible = models.BooleanField()
    leftside = models.IntegerField()
    pageindex = models.IntegerField()
    topside = models.IntegerField()
    bottomside = models.IntegerField(blank=True, null=True)
    rightside = models.IntegerField(blank=True, null=True)
    bookindex = models.IntegerField(blank=True, null=True)
    zoom = models.FloatField(blank=True, null=True)
    media_room = models.OneToOneField(MediaRoom, models.DO_NOTHING)
    owner = models.OneToOneField(MediaParticipant, models.DO_NOTHING, db_column='owner', blank=True, null=True)
    document_id = models.UUIDField(blank=True, null=True)
    audio_owner = models.ForeignKey(AudioParticipant, models.DO_NOTHING, db_column='audio_owner', blank=True, null=True)
    share_file_uri = models.CharField(max_length=2048, blank=True, null=True)
    subscribe_uri = models.CharField(max_length=2048, blank=True, null=True)
    fs_node_id = models.UUIDField(blank=True, null=True)
    start_position = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    pause_position = models.FloatField(blank=True, null=True)
    remote = models.BooleanField(blank=True, null=True)
    vnc_server_address = models.CharField(max_length=255, blank=True, null=True)
    vnc_password = models.CharField(max_length=255, blank=True, null=True)
    connected = models.BooleanField(blank=True, null=True)
    left = models.IntegerField(blank=True, null=True)
    top = models.IntegerField(blank=True, null=True)
    right = models.IntegerField(blank=True, null=True)
    bottom = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'presentation'


class Profile(models.Model):
    profile_type = models.CharField(max_length=3)
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    note = models.CharField(max_length=2000, blank=True, null=True)
    blocked = models.BooleanField()
    user_type = models.CharField(max_length=255, blank=True, null=True)
    avatar_resource = models.UUIDField(blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    conference_template = models.ForeignKey(ConferenceTemplate, models.DO_NOTHING, blank=True, null=True)
    additional_contact = models.CharField(max_length=255, blank=True, null=True)
    additional_contact_privacy = models.CharField(max_length=255, blank=True, null=True)
    additional_contact_type = models.CharField(max_length=10, blank=True, null=True)
    primary_email = models.CharField(max_length=255, blank=True, null=True)
    primary_email_privacy = models.CharField(max_length=255, blank=True, null=True)
    primary_phone = models.CharField(max_length=512, blank=True, null=True)
    primary_phone_privacy = models.CharField(max_length=255, blank=True, null=True)
    tag_list = models.CharField(max_length=1024, blank=True, null=True)
    ldap_login = models.BooleanField(blank=True, null=True)
    event_logo_resource_id = models.UUIDField(blank=True, null=True)
    frame_logo_resource_id = models.UUIDField(blank=True, null=True)
    use_info_block = models.BooleanField(blank=True, null=True)
    info_block_content = models.CharField(max_length=16384, blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)
    disable_create_conference = models.BooleanField(blank=True, null=True)
    disk_space_limit = models.IntegerField(blank=True, null=True)
    dial_at_start = models.BooleanField(blank=True, null=True)
    inform_by_sms = models.BooleanField(blank=True, null=True)
    cascade_type = models.IntegerField(blank=True, null=True)
    max_bitrate = models.BigIntegerField(blank=True, null=True)
    layout_id = models.IntegerField(blank=True, null=True)
    show_own_video = models.BooleanField(blank=True, null=True)
    output_audio_gain = models.IntegerField(blank=True, null=True)
    default_media_group = models.ForeignKey(
        MediaGroup, models.DO_NOTHING, db_column='default_media_group', blank=True,
        null=True)
    main_stream_video_codec = models.SmallIntegerField(blank=True, null=True)
    main_stream_audio_codec = models.SmallIntegerField(blank=True, null=True)
    additional_stream_video_codec = models.SmallIntegerField(blank=True, null=True)
    video_preset = models.SmallIntegerField(blank=True, null=True)
    vvoip_login = models.CharField(max_length=64, blank=True, null=True)
    vvoip_password = models.CharField(max_length=64, blank=True, null=True)
    domain = models.ForeignKey(Domain, models.DO_NOTHING, blank=True, null=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    password = models.BinaryField(blank=True, null=True)
    encryption_type = models.SmallIntegerField(blank=True, null=True)
    encryption_mandatory = models.BooleanField(blank=True, null=True)
    default_event_level = models.IntegerField(blank=True, null=True)
    vvoip_subnet = models.CharField(max_length=32, blank=True, null=True)
    vvoip_extension = models.CharField(unique=True, max_length=64, blank=True, null=True)
    security_level = models.SmallIntegerField()
    referrer_id = models.UUIDField(blank=True, null=True)
    account_expiration_date = models.DateTimeField(blank=True, null=True)
    last_active_date = models.DateTimeField(blank=True, null=True)
    fec_scheme = models.SmallIntegerField(blank=True, null=True)
    adaptive_bitrate = models.BooleanField(blank=True, null=True)
    keep_in_conference = models.BooleanField(blank=True, null=True)
    main_codec_width = models.SmallIntegerField(blank=True, null=True)
    main_codec_height = models.SmallIntegerField(blank=True, null=True)
    main_codec_fps = models.SmallIntegerField(blank=True, null=True)
    additional_codec_width = models.SmallIntegerField(blank=True, null=True)
    additional_codec_height = models.SmallIntegerField(blank=True, null=True)
    additional_codec_fps = models.SmallIntegerField(blank=True, null=True)
    show_own_name = models.BooleanField(blank=True, null=True)
    bfcp_mode = models.SmallIntegerField(blank=True, null=True)
    input_audio_gain = models.IntegerField(blank=True, null=True)
    style_override = models.CharField(max_length=512, blank=True, null=True)
    add_content_screen_mode = models.SmallIntegerField(blank=True, null=True)
    sip_transport_protocol = models.SmallIntegerField(blank=True, null=True)
    external_id = models.CharField(max_length=1024, blank=True, null=True)
    external_data = models.CharField(max_length=128, blank=True, null=True)
    ldap_server = models.ForeignKey(Ldap, models.DO_NOTHING, blank=True, null=True)
    external_avatar_hash = models.CharField(max_length=255, blank=True, null=True)
    interpreter_lang_pair = models.SmallIntegerField()
    broadcast_language = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'
        unique_together = (('profile_type', 'external_id', 'ldap_server'), ('domain', 'login', 'ldap_server'),)


class ProfileForDeleteQueue(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'profile_for_delete_queue'


class Questionnaire(models.Model):
    id = models.UUIDField(primary_key=True)
    last_modified = models.DateTimeField()
    show_results_to_all = models.IntegerField()
    owner = models.ForeignKey(Profile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'questionnaire'


class QuestionnairePoll(models.Model):
    questionnaire = models.OneToOneField(Questionnaire, models.DO_NOTHING, primary_key=True)
    polls = models.OneToOneField(Poll, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'questionnaire_poll'
        unique_together = (('questionnaire', 'polls'),)


class RecoveryPasswordToken(models.Model):
    token_id = models.UUIDField(primary_key=True)
    date = models.DateTimeField()
    profile = models.ForeignKey(Profile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recovery_password_token'


class Registrant(models.Model):
    id = models.UUIDField(primary_key=True)
    registrar = models.CharField(max_length=256, blank=True, null=True)
    aor = models.CharField(max_length=256, blank=True, null=True)
    from_user = models.CharField(max_length=256, blank=True, null=True)
    proxy = models.CharField(max_length=256, blank=True, null=True)
    binding_params = models.CharField(max_length=256, blank=True, null=True)
    user_name = models.CharField(max_length=256, blank=True, null=True)
    password = models.CharField(max_length=256, blank=True, null=True)
    expire = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    sip_transport = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registrant'


class Resources(models.Model):
    resource_id = models.UUIDField(primary_key=True)
    mime_type = models.CharField(max_length=255, blank=True, null=True)
    shared = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    limit_owner_id = models.UUIDField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    object_id = models.UUIDField(blank=True, null=True)
    object_type = models.CharField(max_length=12, blank=True, null=True)
    object_inner_type = models.CharField(max_length=64, blank=True, null=True)
    security_level = models.SmallIntegerField()
    meta_data = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resources'


class RestorePassword(models.Model):
    id = models.UUIDField(primary_key=True)
    code = models.CharField(max_length=6)
    user_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'restore_password'


class ScheduledWorksNotification(models.Model):
    id = models.UUIDField(primary_key=True)
    duration_in_hours = models.IntegerField()
    work_duration_in_hours = models.IntegerField()
    end_show_date = models.DateTimeField(blank=True, null=True)
    show_to_all = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'scheduled_works_notification'


class ScreenShareQuality(models.Model):
    id = models.IntegerField(primary_key=True)
    bandwidth = models.IntegerField()
    fps = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    protocol = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'screen_share_quality'


class Services(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'services'


class Settings(models.Model):
    name = models.CharField(unique=True, max_length=128)
    value = models.CharField(max_length=8192)
    domain = models.ForeignKey(Domain, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings'
        unique_together = (('name', 'domain'),)


class ShortLink(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    full_link = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'short_link'


class SiteCall(models.Model):
    id = models.UUIDField(primary_key=True)
    site_call_account = models.ForeignKey('SiteCallAccount', models.DO_NOTHING, blank=True, null=True)
    accept_call_date = models.DateTimeField(blank=True, null=True)
    call_status = models.CharField(max_length=255)
    end_call_date = models.DateTimeField(blank=True, null=True)
    user_ip = models.CharField(max_length=255)
    ivr_participant_id = models.CharField(max_length=255, blank=True, null=True)
    ivr_publish_uri = models.CharField(max_length=255, blank=True, null=True)
    last_web_update = models.DateTimeField()
    start_call_date = models.DateTimeField(blank=True, null=True)
    web_connect_time = models.DateTimeField(blank=True, null=True)
    publish_uri = models.CharField(max_length=255, blank=True, null=True)
    web_subscribe_uri = models.CharField(max_length=255, blank=True, null=True)
    end_reason = models.CharField(max_length=255, blank=True, null=True)
    video_supported = models.BooleanField(blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    vvoip_address = models.CharField(max_length=255, blank=True, null=True)
    end_reason_details = models.CharField(max_length=255, blank=True, null=True)
    media_server = models.ForeignKey(MediaServer, models.DO_NOTHING, blank=True, null=True)
    publish_screen_uri = models.CharField(max_length=512, blank=True, null=True)
    screen_share_enabled = models.BooleanField()
    record_enabled = models.BooleanField()
    record_resource_id = models.UUIDField(blank=True, null=True)
    record_path = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_call'


class SiteCallAccount(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048, blank=True, null=True)
    vvoip_address = models.CharField(max_length=255)
    vvoip_header = models.CharField(max_length=255)
    video_supported = models.BooleanField()
    max_calls = models.IntegerField()
    max_calls_for_same_ip = models.IntegerField()
    default_user_id = models.CharField(max_length=255, blank=True, null=True)
    max_bitrate = models.IntegerField()
    video_preset = models.SmallIntegerField()
    screen_share_enabled = models.BooleanField()
    web_fps = models.IntegerField()
    web_bitrate = models.IntegerField()
    web_width = models.IntegerField()
    web_height = models.IntegerField()
    record_enabled = models.BooleanField(blank=True, null=True)
    record_keep_days = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_call_account'


class Sms(models.Model):
    sms_id = models.UUIDField(primary_key=True)
    delivery_code = models.IntegerField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    message = models.BinaryField(blank=True, null=True)
    message_id = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)
    smsc_send_date = models.DateTimeField()
    data_coding = models.SmallIntegerField(blank=True, null=True)
    udhi = models.BooleanField(blank=True, null=True)
    send_number = models.IntegerField(blank=True, null=True)
    payer_number = models.CharField(max_length=255, blank=True, null=True)
    cdr_upload_filename = models.CharField(max_length=255, blank=True, null=True)
    source_number = models.CharField(max_length=255, blank=True, null=True)
    protocol_id = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'sms'


class StaticNat(models.Model):
    subnet_mask = models.CharField(max_length=18)
    ip_address = models.CharField(max_length=64)
    ip_external = models.CharField(max_length=64)
    order_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'static_nat'


class SubscribedUsers(models.Model):
    subscription = models.ForeignKey('Subscriptions', models.DO_NOTHING)
    user_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'subscribed_users'


class SubscriptionDetail(models.Model):
    id = models.UUIDField(primary_key=True)
    max_conference_participants = models.IntegerField()
    total_active_conference = models.IntegerField()
    total_audio_participants = models.IntegerField()
    total_web_participants = models.IntegerField()
    billing_account = models.ForeignKey(BillingAccount, models.DO_NOTHING, blank=True, null=True)
    subscription_id = models.UUIDField(unique=True)
    subscription_name = models.CharField(max_length=255, blank=True, null=True)
    conference_type = models.IntegerField(blank=True, null=True)
    max_speakers = models.IntegerField()
    max_recording_storage_days = models.IntegerField()
    iframe_enabled = models.BooleanField()
    voting_enabled = models.BooleanField()
    branding_enabled = models.BooleanField()
    ip_restrictions = models.CharField(max_length=255, blank=True, null=True)
    income_call_to_msisdn_restriction = models.CharField(max_length=255, blank=True, null=True)
    default_media_group = models.ForeignKey(MediaGroup, models.DO_NOTHING, db_column='default_media_group', blank=True,
                                            null=True)
    live_streaming = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription_detail'


class Subscriptions(models.Model):
    subscription_id = models.UUIDField(primary_key=True)
    pin = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    domain_id = models.UUIDField()
    service = models.ForeignKey(Services, models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    activate_date = models.DateTimeField(blank=True, null=True)
    terminate_date = models.DateTimeField(blank=True, null=True)
    block_date = models.DateTimeField(blank=True, null=True)
    unblock_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscriptions'


class SystemAlert(models.Model):
    id = models.UUIDField(primary_key=True)
    server_name = models.CharField(max_length=64)
    object_id = models.CharField(max_length=512, blank=True, null=True)
    occurrence_date = models.DateTimeField()
    resolve_date = models.DateTimeField(blank=True, null=True)
    alert_type = models.IntegerField()
    info_type = models.IntegerField()
    info_json = models.TextField()

    class Meta:
        managed = False
        db_table = 'system_alert'


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True)
    comment = models.CharField(max_length=150, blank=True, null=True)
    connections = models.IntegerField()
    created = models.DateTimeField()
    system = models.BooleanField(blank=True, null=True)
    link = models.CharField(max_length=2048)
    updated = models.DateTimeField()
    conference = models.ForeignKey(Conference, models.DO_NOTHING)
    conference_session = models.ForeignKey(ConferenceSession, models.DO_NOTHING, blank=True, null=True)
    passcode = models.CharField(max_length=16, blank=True, null=True)
    user_role = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket'


class TicketBinding(models.Model):
    id = models.UUIDField(primary_key=True)
    user_session_id = models.UUIDField(unique=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ticket_binding'


class UncommittedResources(models.Model):
    uncommitted_resource_id = models.UUIDField(primary_key=True)
    resource = models.ForeignKey(Resources, models.DO_NOTHING, blank=True, null=True)
    user_session_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uncommitted_resources'


class UserAttribute(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)
    ldap_attribute = models.CharField(max_length=255, blank=True, null=True)
    order_number = models.IntegerField()
    security_level = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'user_attribute'


class UserDevice(models.Model):
    id = models.CharField(primary_key=True, max_length=1024)
    device_token = models.CharField(max_length=512)
    profile = models.ForeignKey(Profile, models.DO_NOTHING)
    operating_system = models.CharField(max_length=32)
    client_type = models.SmallIntegerField()
    create_date = models.DateTimeField()
    device_token_voip = models.CharField(max_length=512, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    user_session_id = models.UUIDField(blank=True, null=True)
    client_assembly = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'user_device'
        unique_together = (('id', 'client_type', 'client_assembly'),)


class UserGroup(models.Model):
    id = models.UUIDField(primary_key=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=2048, blank=True, null=True)
    domain = models.ForeignKey(Domain, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_group'


class UserMarkedMessage(models.Model):
    message = models.OneToOneField(Message, models.DO_NOTHING, primary_key=True)
    profile_id = models.UUIDField()
    chat_room = models.ForeignKey(ChatRoom, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_marked_message'
        unique_together = (('message', 'profile_id'),)


class UserParameter(models.Model):
    attribute = models.OneToOneField(UserAttribute, models.DO_NOTHING, primary_key=True)
    profile = models.ForeignKey(Profile, models.DO_NOTHING)
    value = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_parameter'
        unique_together = (('attribute', 'profile'),)


class UserProperty(models.Model):
    id = models.UUIDField(primary_key=True)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_property'
        unique_together = (('profile', 'key'),)


class UserSessions(models.Model):
    user_session_id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(blank=True, null=True)
    access_time = models.DateTimeField()
    owner_node = models.CharField(max_length=255)
    expire_timeout = models.IntegerField(blank=True, null=True)
    delete_attempt_number = models.IntegerField()
    ip_address = models.CharField(max_length=15)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField()
    token_id = models.UUIDField(blank=True, null=True)
    domain_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_sessions'


class UserSessionsHistory(models.Model):
    user_session_id = models.UUIDField()
    user_id = models.UUIDField(primary_key=True)
    ip_address = models.CharField(max_length=15)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    token_id = models.UUIDField(blank=True, null=True)
    session_end_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_sessions_history'
        unique_together = (('user_id', 'user_session_id'),)


class VcsServerInstance(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'vcs_server_instance'


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'vendor'


class VideoCountRestrictions(models.Model):
    streamsmediaprofile = models.ForeignKey(MediaProfile, models.DO_NOTHING)
    max_video_count = models.IntegerField()
    fps = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'video_count_restrictions'


class VoipCallSettings(models.Model):
    subnet_mask = models.CharField(unique=True, max_length=24)
    order_number = models.IntegerField()
    video_codec = models.IntegerField(blank=True, null=True)
    audio_codec = models.IntegerField(blank=True, null=True)
    additional_channel_video_codec = models.IntegerField(blank=True, null=True)
    sip_transport_protocol = models.IntegerField(blank=True, null=True)
    bfcp_protocol = models.IntegerField(blank=True, null=True)
    encryption = models.IntegerField(blank=True, null=True)
    call_rate_restriction = models.IntegerField(blank=True, null=True)
    ice_support = models.BooleanField(blank=True, null=True)
    audio_only = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'voip_call_settings'


class VvoipRegisterSession(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    profile_id = models.UUIDField()
    session_type = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    expire_time = models.DateTimeField()
    ip = models.CharField(max_length=64, blank=True, null=True)
    agent = models.CharField(max_length=255, blank=True, null=True)
    contacts_json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vvoip_register_session'
        unique_together = (('id', 'profile_id'),)


class VvoipRegisterSessionHistory(models.Model):
    session_id = models.CharField(max_length=255, blank=True, null=True)
    profile_id = models.UUIDField(blank=True, null=True)
    session_type = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    ip = models.CharField(max_length=64, blank=True, null=True)
    agent = models.CharField(max_length=255, blank=True, null=True)
    contacts_json = models.TextField(blank=True, null=True)
    session_end_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vvoip_register_session_history'


class Wbbooks(models.Model):
    wbbook_id = models.UUIDField(primary_key=True)
    wbook_index = models.IntegerField()
    wbook_name = models.CharField(max_length=255, blank=True, null=True)
    whiteboard = models.ForeignKey('Whiteboard', models.DO_NOTHING)
    created_by = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'wbbooks'


class Wbpages(models.Model):
    wbpage_id = models.UUIDField(primary_key=True)
    document_page_id = models.UUIDField(blank=True, null=True)
    page_index = models.IntegerField()
    page_height = models.FloatField()
    page_width = models.FloatField()
    book_fk = models.ForeignKey(Wbbooks, models.DO_NOTHING, db_column='book_fk')

    class Meta:
        managed = False
        db_table = 'wbpages'


class Wbshape(models.Model):
    wbshape_id = models.UUIDField(primary_key=True)
    creator = models.CharField(max_length=255, blank=True, null=True)
    shape_mame = models.CharField(max_length=255, blank=True, null=True)
    shape_type = models.IntegerField()
    page_fk = models.ForeignKey(Wbpages, models.DO_NOTHING, db_column='page_fk')
    create_date = models.DateTimeField()
    creator_participant = models.ForeignKey(ConferenceSessionParticipant, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wbshape'


class WbshapeChange(models.Model):
    wbshape_change_id = models.UUIDField(primary_key=True)
    attr_shape = models.TextField(blank=True, null=True)
    change_date = models.DateTimeField()
    operation_type = models.IntegerField()
    groupcode = models.BigIntegerField(blank=True, null=True)
    groupindex = models.IntegerField(blank=True, null=True)
    change_owner_id = models.UUIDField(blank=True, null=True)
    resource_id = models.UUIDField(blank=True, null=True)
    shape = models.ForeignKey(Wbshape, models.DO_NOTHING)
    svg = models.TextField()

    class Meta:
        managed = False
        db_table = 'wbshape_change'


class Whiteboard(models.Model):
    whiteboard_id = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'whiteboard'
