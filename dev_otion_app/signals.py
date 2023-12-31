from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import Q
from .models import Topics,Entry, CKEditorEntryImages
import re
from .utils import delete_former_image, image_improver, create_picture_tags_CKEditor
from PIL import Image
from django_config.settings import DEBUG, BASE_DIR

if not DEBUG:
    from io import BytesIO
    from urllib import request

## Regenerate the url with the new name
@receiver(pre_save, sender=Topics)
def redefine_topic_url(sender, **kwargs):
    kwargs['instance'].url = slugify(kwargs['instance'].name)

## Post_delete signal for Topics model, in order to delete images after deleting a db entry. We have to override the signal instead of the delete method in order to correctly delete images if we delete entries in bulk.
@receiver(post_delete, sender=Topics)
def topic_delete_images_deletion(sender, **kwargs):
    instance = kwargs['instance']
    if DEBUG:
        delete_former_image('/media/'+instance.image.name)
    else:
        delete_former_image(instance.image.name)

## Regenerate urls with the new name
@receiver(pre_save, sender=Entry)
def redefine_entry_url(sender,**kwargs):
    instance = kwargs['instance']
    instance.url_english = slugify(instance.title_english)
    instance.url_spanish = slugify(instance.title_spanish)
    instance.url_french = slugify(instance.title_french)

## Pre_save signal for Entry model, in order to delete the images that are not longer part of the entry, as well as ensure that the info passed to the database does not contain the CKEditor's automatically generated img tags but picture tags. 
@receiver(pre_save, sender=Entry)
def entry_modified_images_deletion(sender, **kwargs):
    instance = kwargs['instance']
    try: ## If the Entry is not new, we compare the images contained in the entry to save with the ones associated to it in the CKEditorEntryImages helper Db. If an image is no longer in the entry, we assign a null value in the entry value for that image in the database, so the image becomes orphan and will be deleted by the post_save signal.
        ## In prod, the images will be uploaded to a DigitalOcean Spaces server, so the image name will end just before a ? symbol (cause the upload carries GET parameters). This is the reason of adding the ? in the regex below
        excluded_images = CKEditorEntryImages.objects.filter(Q(entry = Entry.objects.get(id=instance.id)) & ~Q(name__in = [name for name in re.findall('<img.*src=".*ckeditor/([^"?]+)', instance.content_english)]))
        if excluded_images.exists():
            excluded_images.update(entry = None)
    except Entry.DoesNotExist:
        pass
    finally: ## No matters if the entry is new or not, we change the auto generated img tags for picture tags containing all the images versions. NOTE: To delete images, it's enough to look on the english content, but here we have to act over the other languages as well
        instance.content_english = create_picture_tags_CKEditor(instance.content_english, 'Blog image')
        instance.content_spanish = create_picture_tags_CKEditor(instance.content_spanish, 'Imagen de blog')
        instance.content_french = create_picture_tags_CKEditor(instance.content_french, 'Image de blog')

## Post_save signal for Entry model, in order to improve the updated images getting webp and avif versions, as well as link the images with the entry in the helper db CKEditorEntryImages. We also delete all images contained in the helper db that are not linked to any entry (db/server cleaning. These images have been loaded in an uncompleted post or have been deleted from its post, so they are taking server space with no use)
@receiver(post_save, sender=Entry)
def entry_image_improver(sender, **kwargs):
    instance = kwargs['instance']
    images = re.findall('<img.*src="([^"]+/ckeditor/([^"?]+))', instance.content_english)
    db_image_recorder = CKEditorEntryImages.objects.filter(Q(name__in = [image[1] for image in images]) & Q(entry__isnull = True))
    new_images = [image for image in images if image[1] in db_image_recorder.values_list('name', flat=True)]
    db_image_recorder.update(entry = Entry.objects.get(id = instance.id))
    for image in new_images:
        ## If the image is catched by new_images constructor it means that it has been added in this save, so we must create AVIF/Webp versions
        if DEBUG: ## In localhost, as images are hosted in the same server, it's possible to open them directly
            image_improver(Image.open(str(BASE_DIR)+image[0]),'media/ckeditor/'+image[1])
        else: ## In prod, images cannot be opened directly as they are hosted in another server, then we have to request the url where they are located and save into a bytes buffer that may be opened by Pillow
            image_improver(Image.open(BytesIO(request.urlopen(image[0]).read())), 'ckeditor/'+image[1])

    ## Cleaning: The images in the db without an assigned entry must be erased from the server (and the db).
    orphan_images = CKEditorEntryImages.objects.filter(entry__isnull = True)
    for image in orphan_images:
        if DEBUG:
            delete_former_image('/media/ckeditor/' + image.name)
        else:
            delete_former_image('ckeditor/'+image.name)
    orphan_images.delete()

## Post_delete signal for Entry model, in order to delete images after deleting a db entry.
@receiver(post_delete, sender=Entry)
def entry_deleted_images_deletion(sender, **kwargs):
    instance = kwargs['instance']
    former_images = re.findall('<img.*src="[^"]+/ckeditor/([^"?]+)', instance.content_english)
    for former_image in former_images:
        if DEBUG:
            delete_former_image('/media/ckeditor/'+former_image)
        else:
            delete_former_image('ckeditor/'+former_image)