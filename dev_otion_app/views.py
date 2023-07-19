import re
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from .models import Entry
from django.utils import timezone


class Dev_otion_TemplateView(TemplateView):
    """
        Generic Template View adapted to this project, in order to carry context data that is used all around the application. TemplateView like views will inherit from this one
    """
    def get_context_data(self):
        context = super().get_context_data()
        context['year'] = timezone.now().strftime('%Y')
        context['current_url'] = self.request.path[4:]
        return context

class Dev_otion_ListView(ListView):
    """
        Generic List View adapted to this project, in order to carry context data that is used all around the application. ListView like views will inherit from this one
    """
    def get_context_data(self):
        context = super().get_context_data()
        context['year'] = timezone.now().strftime('%Y')
        context['current_url'] = self.request.path[4:]
        return context
    
class Dev_otion_DetailView(DetailView):
    """
        Generic Detail View adapted to this project, in order to carry context data that is used all around the application. DetailView like views will inherit from this one
    """
    def get_context_data(self,object):
        context = super().get_context_data()
        context['year'] = timezone.now().strftime('%Y')
        context['current_url'] = re.search('^/[a-z]+/(?P<current_url>[a-zA-z0-9_\-/]+)',self.request.path).group('current_url')
        return context

class IndexView(Dev_otion_TemplateView):
    template_name = 'dev_otion_app/index.html'

class EntryView(Dev_otion_DetailView):
    model = Entry

    def get_context_data(self,object):
        context = super().get_context_data(object)
        lang = re.search('/(?P<lang>[a-z]+)/',self.request.path).group('lang')
        match lang:
            case 'en':
                context['title'] = object.title_english
                context['content'] = object.content_english
            case 'es':
                context['title'] = object.title_spanish
                context['content'] = object.content_spanish
            case 'fr':
                context['title'] = object.title_french
                context['content'] = object.content_french
        return context
    