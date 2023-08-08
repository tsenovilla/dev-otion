from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from .models import Topics,Entry
from PIL import Image
import pillow_avif
import os
import re
from pathlib import Path

## Override of post_delete signal for Topics, in order to delete images after deleting a db entry. We have to override the signal instead of the delete method in order to correctly delete images if we delete entries in bulk.
@receiver(post_delete, sender=Topics)
def topic_delete_images_deletion(sender, instance, **kwargs):
    former_image = instance.image.path
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

@receiver(pre_save, sender=Entry)
def entry_modified_images_deletion(sender, instance, **kwargs):
    try:
        former_entry = Entry.objects.get(id = instance.id)
        former_images = re.findall('<img src="(?P<source>[^"]+)".*/>', former_entry.content_english)
        new_images = re.findall('<img src="(?P<source>[^"]+)".*/>', instance.content_english)
        for former_image in former_images:
            if former_image not in new_images:
                try:
                    os.remove(str(Path(__file__).resolve().parent.parent)+former_image)
                except:
                    pass
                try:
                    os.remove((str(Path(__file__).resolve().parent.parent)+former_image).split('.')[0]+'.webp')
                except:
                    pass
                try:
                    os.remove((str(Path(__file__).resolve().parent.parent)+former_image).split('.')[0]+'.avif')
                except:
                    pass
    except Entry.DoesNotExist:
        pass

@receiver(post_save, sender=Entry)
def entry_image_improver(sender, instance, **kwargs):
    images = re.findall('<img src="(?P<source>[^"]+)".*/>', instance.content_english)
    for image in images:
        image_path = str(Path(__file__).resolve().parent.parent) + image
        img = Image.open(image_path)
        img.save(f'{image_path.split(".")[0]}.webp', format='WEBP')
        img.save(f'{image_path.split(".")[0]}.avif', format='AVIF', codec = 'rav1e', quality = 70) 

@receiver(pre_delete, sender=Entry)
def entry_deleted_images_deletion(sender, instance, **kwargs):
    former_entry = Entry.objects.get(id = instance.id)
    former_images = re.findall('<img src="(?P<source>[^"]+)".*/>', former_entry.content_english)
    for former_image in former_images:
        try:
            os.remove(str(Path(__file__).resolve().parent.parent)+former_image)
        except:
            pass
        try:
            os.remove((str(Path(__file__).resolve().parent.parent)+former_image).split('.')[0]+'.webp')
        except:
            pass
        try:
            os.remove((str(Path(__file__).resolve().parent.parent)+former_image).split('.')[0]+'.avif')
        except:
            pass

    