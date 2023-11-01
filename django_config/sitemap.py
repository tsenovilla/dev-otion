from django.contrib.sitemaps import Sitemap
from dev_otion_app.models import Entry 

class EntrySitemap(Sitemap):
    changefreq = "weekly"  
    priority = 0.8 
    i18n = True

    def items(self):
        return Entry.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()