from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'dev_otion_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path(_('topics'), views.TopicsView.as_view(), name = 'topics'),
    path(_('entry/<slug:url>'), views.EntryView.as_view(), name = 'entry'),
    path(_('contact'), views.ContactView.as_view(), name = 'contact'),
    path('<slug:url>', views.EntrybyTopicView.as_view(), name = 'entrybytopic')
]