from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from .functions import unique_image_name, delete_former_image, image_improver

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
                before_update = Topics.objects.get(id = self.id)
                former_image = before_update.image.url
            except Topics.DoesNotExist:
                pass
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            img2 = img.resize((200,200))
            img2.save(self.image.path)
        except: 
            pass
        else:  ## If there's not error when saving, we try to create avif/webp versions for the images. We also try to delete the former images if they exists
            try:
                if self.image.url != former_image: ## There's a new image
                    delete_former_image(former_image)
                    image_improver(self.image.url)
            except NameError:
                image_improver(self.image.url) ## No former image means new object, so we have to create the improved images, as the path will never be empty, this creates the avif/webp versions   

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

    def __str__(self):
        return self.title_english