from django.db import models
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate
from django.views.generic import DetailView, ListView
from .models import Entry
from django.utils import timezone

class Dev_otion_ListView(ListView):
    """
        Generic List View adapted to this project, in order to carry context data that is used all around the application. ListView like Views will inherit from this one
    """
    def get_context_data(self):
        context = super().get_context_data()
        context['year'] = timezone.now().strftime('%Y')
        return context

class IndexView(Dev_otion_ListView):
    model = Entry
    template_name = "dev_otion_app/index.html"

