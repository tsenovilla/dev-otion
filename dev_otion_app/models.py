from django.db import models
from django.utils import timezone
from PIL import Image
import pillow_avif
from autoslug import AutoSlugField
import os
from .functions import unique_image_name

class Topics(models.Model):
    name = models.CharField(max_length=250)
    ## We upload the images with a unique name provided by uuid4
    image = models.ImageField(
        upload_to = unique_image_name, 
        default = None
    )
    url = AutoSlugField(populate_from='name', max_length=250)

    def save(self, *args, **kwargs):
        """
        Override of save method in order to delete the former images. We also upload an Avif and a WebP version for those images
        """
        try:
            try: ## If we are updating, we get the paths to the former images, in order to delete them
                before_update = Topics.objects.get(id = self.id)
                former_image = before_update.image.path
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
                self.__delete_former_images(former_image=former_image)
                self.__image_improver(former_image=former_image)
            except NameError:
                self.__image_improver(former_image="") ## No former image means new object, so we have to create the improved images, as the path will never be empty, this creates the avif/webp versions

    def __delete_former_images(self, *, former_image):
        """
        This function will delete the former images for each object if a new one has been uploaded.
        """
        if self.image.path != former_image:
            ## If the images are not found on the server (no matters why), or any other exception is raised, we do nothing
            try:
                os.remove(former_image)
            except:
                pass
            try:
                os.remove(former_image.split('.')[0]+'.webp')
            except:
                pass
            try:
                os.remove(former_image.split('.')[0]+'.avif')
            except:
                pass
        

    def __image_improver(self, *, former_image):
        if self.image.path != former_image: ## If we are not updating the image, we do not re-generate avif/webp versions
            img = Image.open(self.image)
            img.save(f'{self.image.name.split(".")[0]}.webp', format='WEBP')
            img.save(f'{self.image.name.split(".")[0]}.avif', format='AVIF', codec = 'rav1e', quality = 70) ## Following the recommendations from pillow_avif's creator, we set codec and quality

    def __str__(self):
        return self.name

class Entry(models.Model):
    ## For each language supported by the app, and each entry field containing text, we include a field supporting that field in each language. As this is dinamic content, we save it in such a way in order to make the app more scallable. If we store the translations in the message files, we would need to update them each time an entry is loaded
    title_english = models.CharField(max_length = 250)
    title_spanish = models.CharField(max_length = 250)
    title_french = models.CharField(max_length = 250)
    author = models.CharField(max_length = 100)
    pub_date = models.DateField(default=timezone.now)
    content_english = models.TextField(default = '')
    content_spanish = models.TextField(default = '')
    content_french = models.TextField(default = '')
    url_english = AutoSlugField(populate_from='title_english', max_length = 250)
    url_spanish = AutoSlugField(populate_from='title_spanish', max_length = 250)
    url_french = AutoSlugField(populate_from='title_french', max_length = 250)
    topic = models.ForeignKey(Topics, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return self.title_english