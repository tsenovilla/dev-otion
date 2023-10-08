from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Topics,Entry, CKEditorEntryImages
import re
from .utils import delete_former_image, image_improver, create_picture_tags_CKEditor

## Override of post_delete signal for Topics model, in order to delete images after deleting a db entry. We have to override the signal instead of the delete method in order to correctly delete images if we delete entries in bulk.
@receiver(post_delete, sender=Topics)
def topic_delete_images_deletion(sender, instance, **kwargs):
    delete_former_image(instance.image.url)

## Override of pre_save signal for Entry model, in order to delete the images that are not longer part of the entry, as well as ensure that the info passed to the database does not contain the CKEditor's automatically generated img tags but picture tags. 
@receiver(pre_save, sender=Entry)
def entry_modified_images_deletion(sender, instance, **kwargs):
    try: ## If the Entry is not new, we compare the images contained in the entry to save with the ones associated to it in the CKEditorEntryImages helper Db. If an image is no longer in the entry, we assign a null value in the entry value for that image in the database, so the image becomes orphan and will be deleted by the post_save signal.
        former_images = CKEditorEntryImages.objects.filter(entry = Entry.objects.get(id = instance.id))
        new_images = re.findall('<img.*src="(?P<source>[^"]+)".*>', instance.content_english)
        for former_image in former_images:
            if former_image.name not in new_images:
                former_image.entry = None
                former_image.save()
    except Entry.DoesNotExist:
        pass
    finally: ## No matters if the entry is new or not, we change the auto generated img tags for picture tags containing all the images versions. NOTE: To delete images, it's enough to look on the english content, but here we have to act over the other languages as well
        instance.content_english = create_picture_tags_CKEditor(instance.content_english, 'Blog image')
        instance.content_spanish = create_picture_tags_CKEditor(instance.content_spanish, 'Imagen de blog')
        instance.content_french = create_picture_tags_CKEditor(instance.content_french, 'Image de blog')

## Override on post_save signal for Entry model, in order to improve the updated images getting webp and avif versions, as well as link the images with the entry in the helper db CKEditorEntryImages. We also delete all images contained in the helper db that are not linked to any entry (db/server cleaning. These images have been loaded in an uncompleted post, so they are taking server space with no use)
@receiver(post_save, sender=Entry)
def entry_image_improver(sender, instance, **kwargs):
    images = re.findall('<img.*src="(?P<source>[^"]+)".*>', instance.content_english)
    for image in images:
        try: ## If the image is catched by the instruction below, it means that it has been added in this save, so we must de-orphan the image and create AVIF/Webp versions
            db_image_recorder = CKEditorEntryImages.objects.get(name = image.split('/')[-1], entry__isnull = True)
            db_image_recorder.entry = Entry.objects.get(id = instance.id)
            db_image_recorder.save()
            image_improver(image)
        except CKEditorEntryImages.DoesNotExist: ## This happens if the image is in the entry from a previous version (if entry is not null). So there's nothing to do
            pass
    ## Cleaning: The images in the db without an assigned entry must be erased from the server (and the db).
    orphan_images = CKEditorEntryImages.objects.filter(entry__isnull = True)
    for image in orphan_images:
        delete_former_image('/media/ckeditor/' + image.name)
    orphan_images.delete()

## Override of post_delete signal for Entry model, in order to delete images after deleting a db entry.
@receiver(post_delete, sender=Entry)
def entry_deleted_images_deletion(sender, instance, **kwargs):
    former_images = re.findall('<img.*src="(?P<source>[^"]+)".*>', instance.content_english)
    for former_image in former_images:
        delete_former_image(former_image)