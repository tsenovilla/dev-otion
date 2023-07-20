from django.db import models
from django.utils import timezone
from uuid import uuid4
import os

class Topics(models.Model):
    name = models.CharField(max_length=250)
    ## We upload the images with a unique name provided by uuid4
    image = models.ImageField(
        upload_to = 
        lambda instance, filename: 'dev_otion_app/static/dev_otion_app/img/'+uuid4().hex+'.'+filename.split('.')[-1], 
        default=None
        )
    
    ## This function, used in combination with an override on the save method, will delete the former image for each object if a new one has been uploaded
    def delete_former_image(self):
        try:
            before_update = Topics.objects.get(id=self.id)
            if before_update.image and self.image:
                os.remove(before_update.image.path)
        except Topics.DoesNotExist: ## If the object has not a former image, we do nothing
            pass

    ## Override of save method in order to delete the former image
    def save(self):
        self.delete_former_image()
        super().save()
    
    def __str__(self):
        return self.name

class Entry(models.Model):
    ## For each language supported by the app, and each entry field containing text, we include a field supporting that field in each language. As this is dinamic content, we save it in such a way in order to make the app more scallable. If we store the translations in the message files, we would need to update them each time an entry is loaded
    title_english = models.CharField(max_length=250)
    title_spanish = models.CharField(max_length=250)
    title_french = models.CharField(max_length=250)
    pub_date = models.DateField(default=timezone.now)
    content_english = models.TextField(default="")
    content_spanish = models.TextField(default="")
    content_french = models.TextField(default="")
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title_english