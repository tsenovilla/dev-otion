from django.contrib import admin
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Topics, Entry

class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField:{'widget':CKEditorUploadingWidget()}
    }

admin.site.register(Topics)
admin.site.register(Entry, EntryAdmin)