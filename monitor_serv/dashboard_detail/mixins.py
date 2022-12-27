from django.views import generic


class ServerAnalysisDetailMixin(generic.DetailView):
    cmd: str = None