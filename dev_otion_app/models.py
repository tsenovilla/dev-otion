from django.db import models
from django.utils import timezone
from django.utils.translation import get_language
from django.urls import reverse
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from .utils import unique_image_name, delete_former_image, image_improver
from django_config.settings import DEBUG

if not DEBUG:
    from io import BytesIO
    from django.core.files.storage import default_storage as storage

class Topics(models.Model):
    name = models.CharField(max_length=250)
    ## We upload the images with a unique name provided by uuid4
    image = models.ImageField(
        upload_to = unique_image_name, 
        default = None
    )
    url = AutoSlugField(populate_from='name', max_length=250)

    def save(self, *args, **kwargs):
        ## Override of save method in order to delete the former images. We also upload an Avif and a WebP version for those images. As we pass information from the pre_save to the post_save, it is better to override the method instead of using signals
        try:
            try: ## If we are updating, we get the paths to the former images, in order to delete them
                former_image = Topics.objects.get(id = self.id).image.name
            except Topics.DoesNotExist:
                pass
            super().save(*args, **kwargs)
        except: 
            pass
        else:  ## If there's not error when saving, we try to create avif/webp versions for the images. We also try to delete the former images if they exists
            try:
                if self.image.name != former_image: ## There's a new image
                    if DEBUG:
                        delete_former_image('/media/'+former_image)
                        image_improver(Image.open(self.image), 'media/'+self.image.name)
                    else:
                        delete_former_image(former_image)
                        image_improver(Image.open(self.image), self.image.name)
            except NameError:
                if DEBUG:
                    image_improver(Image.open(self.image), 'media/'+self.image.name) ## No former image means new object, so we have to create the improved images, as the path will never be empty, this creates the avif/webp versions   
                else:
                    image_improver(Image.open(self.image), self.image.name)

    def __str__(self):
        return self.name

class Entry(models.Model):
    ## For each language supported by the app, and each entry field containing text, we include a field supporting that field in each language. As this is dinamic content, we save it in such a way in order to make the app more scallable. If we store the translations in the message files, we would need to update them each time an entry is loaded
    title_english = models.CharField(max_length = 250)
    title_spanish = models.CharField(max_length = 250)
    title_french = models.CharField(max_length = 250)
    author = models.CharField(max_length = 100)
    pub_date = models.DateField(default = timezone.now)
    content_english = RichTextUploadingField(default = '')
    content_spanish = models.TextField(default = '')
    content_french = models.TextField(default = '')
    url_english = AutoSlugField(populate_from = 'title_english', max_length = 250)
    url_spanish = AutoSlugField(populate_from = 'title_spanish', max_length = 250)
    url_french = AutoSlugField(populate_from = 'title_french', max_length = 250)
    topic = models.ForeignKey(Topics, on_delete = models.CASCADE, default = None)

    def get_absolute_url(self):
        language = get_language()
        match language:
            case 'en':
                args = [str(self.url_english)]
            case 'es':
                args = [str(self.url_spanish)]
            case 'fr':
                args = [str(self.url_french)]
        return reverse('dev_otion_app:entry', args=args)

    def __str__(self):
        return self.title_english
    
class CKEditorEntryImages(models.Model):
    ## Helper db where CKEditor's uploaded images are linked to their related entry, or to null if they don't appear in any entry, thus if they must be erased from the server 
    name = models.CharField(max_length = 250)
    entry = models.ForeignKey(Entry, on_delete = models.CASCADE, null = True)