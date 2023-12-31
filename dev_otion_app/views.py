import re
from django.views.generic.base import View
from django.views.generic import DetailView, ListView, TemplateView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.templatetags.static import static
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from .models import Topics,Entry
from .utils import reverse_self_url, ContactForm
import os

# This base View contains the common data used by each class in the app. The other views must inherit from it in first instance to retrieve this data, then from the specific general view needed.
class Dev_otion_View(View):
    def get_context_data(self):
        context = {}
        context['year'] = timezone.now().strftime('%Y')
        context['lang'] =  re.search('^/(?P<lang>[a-z]+)/',self.request.path).group('lang')
        context['reverted_urls'] = reverse_self_url(self, languages = ['en','es','fr'], current_language = context['lang'])
        return context


class IndexView(Dev_otion_View, TemplateView):
    template_name = 'dev_otion_app/index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['last_entries'] = []
        last_entries = Entry.objects.all().order_by('-pub_date')[:8]
        for entry in last_entries:
            entry_topic = Topics.objects.get(id = entry.topic_id)
            match context['lang']:
                case 'en':
                    title = entry.title_english
                    url = entry.url_english
                case 'es':
                    title = entry.title_spanish
                    url = entry.url_spanish
                case 'fr':
                    title = entry.title_french
                    url = entry.url_french
            context['last_entries'].append({'title':title,'url':url,'image':entry_topic.image})
        return context

class TopicsView(Dev_otion_View, ListView):
    model = Topics
    template_name = 'dev_otion_app/topics.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['topics'] = self.object_list ## As ListView is the second parent class, we need to explicitly assign the object_list to the data
        return context

class EntrybyTopicView(Dev_otion_View, ListView):
    model = Entry
    template_name = 'dev_otion_app/entrybytopic.html'

    def get_queryset(self):
        selected_topic = Topics.objects.get(url = self.kwargs['url'])
        return Entry.objects.filter(topic = selected_topic).order_by('-pub_date')
    
    def get_context_data(self):
        context = super().get_context_data()
        context['topic'] = self.kwargs['url'].capitalize()
        context['entries'] = []
        for entry in self.object_list:
            match context['lang']:
                case 'en':
                    title = entry.title_english
                    url = entry.url_english
                case 'es':
                    title = entry.title_spanish
                    url = entry.url_spanish
                case 'fr':
                    title = entry.title_french
                    url = entry.url_french
            context['entries'].append({'title':title, 'pub_date':entry.pub_date,'url':url,'author':entry.author})
        return context
    
class EntryView(Dev_otion_View, DetailView):
    model = Entry
    template_name = 'dev_otion_app/entry.html'

    def get_object(self):
        context = super().get_context_data()
        match context['lang']:
            case 'en':
                return Entry.objects.get(url_english = self.kwargs['url'])
            case 'es':
                return Entry.objects.get(url_spanish = self.kwargs['url'])
            case 'fr':
                return Entry.objects.get(url_french = self.kwargs['url'])

    def get_context_data(self,object):
        context = super().get_context_data()
        selected_entry = Entry.objects.get(id = self.object.id)
        context['reverted_urls'] = reverse_self_url(self, languages = ['en','es','fr'], current_language = context['lang'], languages_slugs = {'en':selected_entry.url_english, 'es':selected_entry.url_spanish, 'fr':selected_entry.url_french})
        context['topic_url'] = Topics.objects.get(id = self.object.topic_id).url
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

class ContactView(Dev_otion_View, TemplateView):
    template_name = 'dev_otion_app/contact.html'

    def get_context_data(self):
        context = super().get_context_data()
        try: # We will only pass OK alerts as session elements, due to if something goes wrong with the post we continue in POST request method, so it's enough with use a render_to_response. We have to remove the alert from the session as we are using it just once
            context['alert'] = self.request.session.pop('alert')
            context['alert_type'] = self.request.session.pop('alert_type')
        except KeyError:
            pass
        return context

    def post(self, request):
        submitted_form = ContactForm(request.POST)
        context = super().get_context_data()
        if submitted_form.is_valid(): # If the form is well filled, we try to send an e-mail to dev-otion with the requested post. We use Brevo as mail provider
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = os.environ['BREVO_API_KEY']
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = 'New post request'
            sender = {'email':'tspscgs@gmail.com'}
            html_content = f'<html><body><p>{submitted_form.cleaned_data["message"]}</p></body></html>'
            to = [{'email':'dev-otion@hotmail.com'}]
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to = to, html_content = html_content, sender = sender, subject = subject)
            try:
                api_instance.send_transac_email(send_smtp_email)
                request.session['alert'] = _('Thank you for your message! We will get back to you as soon as possible')
                request.session['alert_type'] = 'OK'
                return HttpResponseRedirect(reverse('dev_otion_app:contact'))
            except ApiException:
                context['alert'] = _('Something went wrong :( Please try again in a few minutes')
                context['alert_type'] = 'KO'
        else: # We show the error provided by the Django's Form object to the user
            context['alert_type'] = 'KO'
            context['message'] = request.POST['message']
            if 'message' in submitted_form.errors:
                context['alert'] = _('Message: ') + re.search('<li>(?P<error>.*)</li>', str(submitted_form.errors['message'])).group('error')
                context['error'] = 'message'
        return self.render_to_response(context)