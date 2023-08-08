from django.contrib import admin
from django.urls import path,include
from django.conf.urls.i18n import i18n_patterns as i18n
from django.conf.urls.static import static
from . import settings

urlpatterns = i18n(
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('',include('dev_otion_app.urls', namespace = 'dev_otion_app'))
) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)