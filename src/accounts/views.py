from django.views.generic import TemplateView
from ics.models import Storage


class WelcomePageView(TemplateView):
    template_name = 'registration/welcome/welcome.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['storages'] = Storage.objects.all()
        context["is_welcome"] = True
        return context
