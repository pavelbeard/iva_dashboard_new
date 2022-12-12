from django.views.generic import edit


class AddServerForm(edit.FormView):

    def form_valid(self, form):

        return super().form_valid(form)
