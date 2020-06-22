from django.views.generic import TemplateView


class UIView(TemplateView):

    template_name = 'ui/index.html'