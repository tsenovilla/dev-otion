from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Topics
import os

## Override of post_delete signal for Topics, in order to delete images after deleting a db entry. We have to override the signal instead of the delete method in order to correctly delete images if we delete entries in bulk.
@receiver(post_delete, sender=Topics)
def topic_post_delete(sender, instance,**kwargs):
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