from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Topics,Entry
import re
from .functions import delete_former_image, image_improver

## Override of post_delete signal for Topics model, in order to delete images after deleting a db entry. We have to override the signal instead of the delete method in order to correctly delete images if we delete entries in bulk.
@receiver(post_delete, sender=Topics)
def topic_delete_images_deletion(sender, instance, **kwargs):
    delete_former_image(instance.image.url)

## Override of pre_save signal for Entry model, in order to delete the images that are not longer part of the entry, as well as ensure that the info passed to the database does not contain the CKEditor's automatically generated img tags but picture tags. 
@receiver(pre_save, sender=Entry)
def entry_modified_images_deletion(sender, instance, **kwargs):
    try: ## If the Entry is not new, we compare the source path for images contained in the previous entry with the new ones. If there's an image in the pre-saved post that's not longer present, we delete it.
        former_entry = Entry.objects.get(id = instance.id)
        former_images = re.findall('<img.*src="(?P<source>[^"]+)".*>', former_entry.content_english)
        new_images = re.findall('<img.*src="(?P<source>[^"]+)".*>', instance.content_english)
        for former_image in former_images:
            if former_image not in new_images:
                delete_former_image(former_image)
    except Entry.DoesNotExist:
        pass
    finally: ## No matters if the entry is new or not, we change the auto generated img tags for picture tags containing all the images versions. NOTE: To delete images, it's enough to look on the english content, but here we have to act over the other languages as well
        instance.content_english = re.sub('<img.*src="(?P<source>[^"]+)".*>', 
                                lambda match: 
                                f'<picture><source srcset="{match.group("source").split(".")[0]}.avif" type="image/avif"><source srcset="{match.group("source").split(".")[0]}.webp" type="image/webp"><img src="{match.group("source")}" alt="Blog image" loading="lazy"></picture>',
                                instance.content_english
                            )
        instance.content_spanish = re.sub('<img.*src="(?P<source>[^"]+)".*>', 
                                lambda match: 
                                f'<picture><source srcset="{match.group("source").split(".")[0]}.avif" type="image/avif"><source srcset="{match.group("source").split(".")[0]}.webp" type="image/webp"><img src="{match.group("source")}" alt="Imagen de blog" loading="lazy"></picture>',
                                instance.content_spanish
                            )
        instance.content_french = re.sub('<img.*src="(?P<source>[^"]+)".*>', 
                                lambda match: 
                                f'<picture><source srcset="{match.group("source").split(".")[0]}.avif" type="image/avif"><source srcset="{match.group("source").split(".")[0]}.webp" type="image/webp"><img src="{match.group("source")}" alt="Image de blog" loading="lazy"></picture>',
                                instance.content_french
                            )

## Override on post_save signal for Entry model, in order to improve the updated images getting webp and avif versions
@receiver(post_save, sender=Entry)
def entry_image_improver(sender, instance, **kwargs):
    images = re.findall('<img.*src="(?P<source>[^"]+)".*>', instance.content_english)
    for image in images:
        image_improver(image)

## Override of post_delete signal for Entry model, in order to delete images after deleting a db entry.
@receiver(post_delete, sender=Entry)
def entry_deleted_images_deletion(sender, instance, **kwargs):
    former_images = re.findall('<img.*src="(?P<source>[^"]+)".*>', instance.content_english)
    for former_image in former_images:
        delete_former_image(former_image)