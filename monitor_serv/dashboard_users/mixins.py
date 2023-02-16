# from bootstrap_modal_forms.generic import BSModalCreateView
# from django import http

# class SignupLogicMixin(BSModalCreateView):
#     def form_valid(self, form):
#         user = form.save()
#         # user = form.save(commit=False)
#         # user.is_active = False
#         # user.save()
#         # form.save_m2m()
#         return http.HttpResponseRedirect(self.success_url)
