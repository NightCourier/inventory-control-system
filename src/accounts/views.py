from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from ics.models import Storage


class WelcomePageView(PermissionRequiredMixin, TemplateView):
    template_name = 'registration/welcome/welcome.html'
    permission_required = 'ics.view_product'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['storages'] = Storage.objects.all()
        context["is_welcome"] = True
        return context
