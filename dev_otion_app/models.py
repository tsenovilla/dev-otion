from django.db import models
from django.utils import timezone

class Entry(models.Model):
    ## For each language supported by the app, and each entry field containing text, we include a field supporting that field in each language. As this is dinamic content, we save it in such a way in order to make the app more scallable. If we store the translations in the message files, we would need to update them each time an entry is loaded
    title_english = models.CharField(max_length=250)
    title_spanish = models.CharField(max_length=250)
    title_french = models.CharField(max_length=250)
    pub_date = models.DateField(default=timezone.now)
    content_english = models.TextField(default="")
    content_spanish = models.TextField(default="")
    content_french = models.TextField(default="")

    def __str__(self):
        return self.title_english