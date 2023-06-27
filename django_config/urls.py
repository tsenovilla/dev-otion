from django.contrib import admin
from django.urls import path,include
from django.conf.urls.i18n import i18n_patterns as i18n

urlpatterns = i18n(
    path("admin/", admin.site.urls),
    path("",include("dev_otion_app.urls"))
)