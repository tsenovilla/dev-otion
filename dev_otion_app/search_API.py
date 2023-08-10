from django.http import JsonResponse
from django.views.generic.base import View
from django.urls import reverse
from django.db.models import Q
from .models import Entry
import json
import re

# This view manage Fetch API requests sent by the search bar located in the header. It looks for any entry containing the user input
class SearchView(View):
    def post(self, request):
        input = json.loads(request.body).get('input')
        lang =  re.search('^/(?P<lang>[a-z]+)/',self.request.path).group('lang')
        response = {}
        query = Q()
        match lang:
            case 'en':
                for word in input.split():
                    query&=Q(title_english__icontains = word)
                entrys = Entry.objects.filter(query).order_by('-pub_date')[:4] ## We return entries ordered by pub_date, with a maximum of 4. This is to not overload the entries showed to the user, as it may do a better search the results showed are not exactly the desired ones
                for entry in entrys:
                    response[entry.title_english] = reverse('dev_otion_app:entry', kwargs = {'url': entry.url_english})
            case 'es':
                for word in input.split():
                    query&=Q(title_spanish__icontains = word)
                entrys = Entry.objects.filter(query).order_by('-pub_date')[:4]
                for entry in entrys:
                    response[entry.title_spanish] = reverse('dev_otion_app:entry', kwargs = {'url': entry.url_spanish})
            case 'fr':
                for word in input.split():
                    query&=Q(title_french__icontains = word)
                entrys = Entry.objects.filter(query).order_by('-pub_date')[:4]
                for entry in entrys:
                    response[entry.title_french] = reverse('dev_otion_app:entry', kwargs = {'url': entry.url_french})
        return JsonResponse(response)