from django.urls import path

from . import views

appname = 'dev_otion_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('topics', views.TopicsView.as_view(), name='topics'),
    path('topics/<slug:url>', views.EntrybyTopicView.as_view(), name='entrybytopic'),
    path('entry/<slug:url>', views.EntryView.as_view(), name='entry')
]