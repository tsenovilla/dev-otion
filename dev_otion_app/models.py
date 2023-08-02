from django.db import models
from django.utils import timezone
from uuid import uuid4
from PIL import Image
import pillow_avif
import os
import inspect

def unique_image_name (instance, filename):
    """
    This function is used by ImageField's upload_to in order to get a unique name for an updated image, obtained via uuid4. 
    WARNING: You might be tempted to use a lambda function instead of this one. That works perfectly when the application is running, but it fails when we make Django migrations. This is due to lambda functions cannot be serialized, which is a requirement for Django's migration framework. Therefore, to achieve a more consistent app, it is better to use this one.
    """
    return 'dev_otion_app/static/dev_otion_app/img/'+uuid4().hex+'.'+filename.split('.')[-1]

class Topics(models.Model):
    name = models.CharField(max_length=250)
    ## We upload the images with a unique name provided by uuid4
    image = models.ImageField(
        upload_to = unique_image_name, 
        default = None
    )
    
    def save(self):
        """
        Override of save method in order to delete the former images. We also upload an Avif and a WebP version for those images
        """
        try:
            try: ## If we are updating, we get the paths to the former images, in order to delete them
                before_update = Topics.objects.get(id = self.id)
                former_image = before_update.image.path
            except Topics.DoesNotExist:
                pass
            super().save()
        except: 
            pass
        else:  ## If there's not error when saving, we try to create avif/webp versions for the images. We also try to delete the former images if they exists
            try:
                self.__delete_former_images(former_image=former_image)
                self.__image_improver(former_image=former_image)
            except NameError:
                self.__image_improver(former_image="") ## No former image means new object, so we have to create the improved images, as the path will never be empty, this creates the avif/webp versions


    
    def delete(self):
        """
        Override of delete method in order to delete the images from the server.
        """
        to_delete = Topics.objects.get(id=self.id)
        former_image = to_delete.image.path
        self.__delete_former_images(former_image=former_image)
        super().delete()

    def __delete_former_images(self, *, former_image):
        """
        This function will delete the former images for each object if a new one has been uploaded or the topic is being deleted
        """
        if self.image.path != former_image or inspect.getframeinfo(inspect.currentframe().f_back).function == 'delete': 
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