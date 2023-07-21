import re
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View
from django.views.generic import DetailView, ListView, TemplateView
from .models import Topics,Entry
from django.utils import timezone

class Dev_otion_View(View):
    '''
        This base View contains the common data used by each class in the app. The other views must inherit from it in first instance to retrieve this data, then from the specific general view needed.
    '''
    def get_context_data(self):
        context = {}
        context['year'] = timezone.now().strftime('%Y')
        url_explorer = re.search('^/(?P<lang>[a-z]+)/(?P<current_url>[a-zA-z0-9_\-/]+)*',self.request.path)
        context['lang'] = url_explorer.group('lang')
        context['current_url'] = url_explorer.group('current_url') if url_explorer.group('current_url') else ''
        return context


class IndexView(Dev_otion_View, TemplateView):
    template_name = 'dev_otion_app/index.html'

class TopicsView(Dev_otion_View, ListView):
    model = Topics
    
    def get_context_data(self):
        context = super().get_context_data()
        context['topics'] = self.object_list ## As ListView is the second parent class, we need to explicitly assign the object_list to the data
        return context
    
class EntryView(Dev_otion_View, DetailView):
    model = Entry

    def get_context_data(self,object):
        context = super().get_context_data()
        match context['lang']:
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
