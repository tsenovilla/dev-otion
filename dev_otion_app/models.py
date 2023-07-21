from django.db import models, transaction
from django.utils import timezone
from uuid import uuid4
from PIL import Image
import pillow_avif
import os
from io import BytesIO


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
    image_webp = models.ImageField(
        default = None,
        blank = True
    )
    image_avif = models.ImageField(
        default = None,
        blank = True
    )
    
    def save(self):
        """
        Override of save method in order to delete the former images. We also upload an Avif and a WebP version for those images
        """
        try:
            try: ## If we are updating, we get the paths to the former images, in order to delete them
                before_update = Topics.objects.get(id = self.id)
                name = before_update.image.name
                former_image = before_update.image.path
                former_image_webp = before_update.image_webp.path
                former_image_avif = before_update.image_avif.path
            except Topics.DoesNotExist:
                pass

            with transaction.atomic(): ## We start an atomic transaction before saving. This allows us to manage if the webp/avif images has been correctly loaded. If there's an error, we do not delete the previous images and we do not update the database
                super().save()
                self.__image_webp_converter()
                self.__image_avif_converter()
            
            ## If there's not rollback, we delete the former images, if they exist. 
            try:
                self.__delete_former_image(name=name, former_image=former_image, former_image_webp=former_image_webp, former_image_avif=former_image_avif)
            except NameError:
                pass

        except:
            pass
    
    def delete(self):
        """
        Override of delete method in order to delete the images from the server.
        """
        to_delete = Topics.objects.get(id=self.id)
        try:
            os.remove(to_delete.image.path)
        except:
            pass
        try:
            os.remove(to_delete.image_webp.path)
        except:
            pass
        try:
            os.remove(to_delete.image_avif.path)
        except:
            pass
        super().delete()

    ## This guards are used in order to avoid reentrancy in the methods 'image_webp_converter' and 'image_avif_converter', as we save Webp and AVIF versions, the save method is called several times, and so those methods
    __reentrancy_guards = [False]*2

    def __delete_former_image(self, *, name, former_image, former_image_webp, former_image_avif):
        """
        This function will delete the former images for each object if a new one has been uploaded.
        """
        ## If self.image.name is not equal to the one stored in the db, then a new image have been uploaded
        if self.image.name != name: 
            ## If the images are not found on the server (no matters why), or any other exception is raised, we do nothing
            try:
                os.remove(former_image)
            except:
                pass
            try:
                os.remove(former_image_webp)
            except:
                pass
            try:
                os.remove(former_image_avif)
            except:
                pass

    def __image_webp_converter(self):
        ## The order in the if statement below is ESSENTIAL. When we create a new Topic, due to the logic in the save method, the first save is done with image_webp empty. Then image_webp.name is None, so if we try to split it, an exception is raised and we pass automatically to the except block. Therefore, it is mandatory to check if we are in the creation of the topic first (by checking that the webp image's name is not defined), in order to avoid trying a split in a None object
        if self.image_webp.name == None or self.image.name.split('.')[0] != self.image_webp.name.split('.')[0] and not self.__reentrancy_guards[0]:
            img = Image.open(self.image)
            webp_io = BytesIO()
            img.save(webp_io, format='WEBP')
            self.image_webp.save(f'{self.image.name.split(".")[0]}.webp', webp_io)
            self.__reentrancy_guards[0] = True

    def __image_avif_converter(self):
        if self.image_avif.name == None or self.image.name.split('.')[0] != self.image_avif.name.split('.')[0] and not self.__reentrancy_guards[1]:
            img = Image.open(self.image)
            avif_io = BytesIO()
            img.save(avif_io, format='AVIF', codec = 'rav1e', quality = 70) ## Following the recommendations from pillow_avif's creator, we set codec and quality
            self.image_avif.save(f'{self.image.name.split(".")[0]}.avif', avif_io)
            self.__reentrancy_guards[1] = True

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