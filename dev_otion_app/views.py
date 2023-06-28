from django.db import models
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.views.generic import DetailView, ListView
from .models import Entry

class IndexView(ListView):
    model = Entry
    template_name = "dev_otion_app/index.html"
