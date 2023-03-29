from django.contrib.sessions.models import Session


class UserSessionMixin:
    def get_user_id_from_session(self, request):
        session_key = request.session.session_key

        try:
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('_auth_user_id')
            return user_id
        except Session.DoesNotExist:
            return None

    def get_session(self, request):
        session_key = request.session.session_key
        try:
            session = Session.objects.get(session_key=session_key)
            return session
        except Session.DoesNotExist:
            return None
